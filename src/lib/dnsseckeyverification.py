from typing import Union, Dict, List
from enum import Enum
import unbound
import hashlib
import base64
import re
import subprocess


def email2location(email_address: str, tag: str = "_openpgpkey") -> str:
    """
    Implements RFC 7929, section 3
    https://tools.ietf.org/html/rfc7929#section-3
    :param email_address:
    :param tag:
    :return:
    """
    split = email_address.split("@")
    if len(split) == 2:
        local = split[0]
        domain = split[1]
        hash = hashlib.sha256()
        hash.update(local.encode('utf-8'))
        digest = base64.b16encode(hash.digest()[0:28])\
            .decode("utf-8")\
            .lower()
        return digest+"."+tag+"."+domain
    else:
        # Error
        return "Error"


class Validity(Enum):
    VALID = 1
    REVOKED = 2
    PROVEN_NONEXISTENCE = 3
    RESULT_NOT_SECURE = 4
    BOGUS_RESULT = 5
    ERROR = 9


class NoKey:
    pass


class KeyInfo:
    def __init__(self, email=None, key=None):
        self.email = email
        self.key = key

    @staticmethod
    def from_rpm_key_object(userid: str, raw_key: bytes):
        # TODO: error handling
        email = re.search('<(.*@.*)>', userid).group(1)
        key = raw_key.decode('ascii').split('\n')
        start = next(i for i in range(0, len(key)) if key[i] == '-----BEGIN PGP PUBLIC KEY BLOCK-----')
        stop = next(i for i in range(0, len(key)) if key[i] == '-----END PGP PUBLIC KEY BLOCK-----')
        cat_key = ''.join(key[start + 2:stop - 1]).encode('ascii')

        ret_val = KeyInfo()
        ret_val.email = email
        ret_val.key = cat_key
        return ret_val


class DNSSECKeyVerification:
    # Mapping from email address to b64 encoded public key or NoKey in case of proven nonexistence
    __cache: Dict[str, Union[str, NoKey]] = {}

    @staticmethod
    def __cache_hit(key_union: Union[str, NoKey], input_key_string: str) -> Validity:
        if key_union == input_key_string:
            return Validity.VALID
        elif key_union is NoKey:
            return Validity.PROVEN_NONEXISTENCE
        else:
            return Validity.REVOKED

    @staticmethod
    def __cache_miss(input_key: KeyInfo) -> Validity:
        RR_TYPE_OPENPGPKEY = 61
        ctx = unbound.ub_ctx()
        ctx.config("/vagrant/unbound/libunbound.conf")
        ctx.add_ta_file("/vagrant/root-server/root.zone.signed")
        status, result = ctx.resolve(email2location(input_key.email), RR_TYPE_OPENPGPKEY, unbound.RR_CLASS_IN)
        if status != 0:
            return Validity.ERROR
        if result.bogus:
            return Validity.BOGUS_RESULT
        if not result.secure:
            return Validity.RESULT_NOT_SECURE
        if result.nxdomain:
            return Validity.PROVEN_NONEXISTENCE
        if not result.havedata:
            # TODO: what kind of result is this???
            return Validity.ERROR
        else:
            data = result.data.as_raw_data()[0]
            dns_data_b64 = base64.b64encode(data)
            if dns_data_b64 == input_key.key:
                return Validity.VALID
            else:
                return Validity.REVOKED

    @staticmethod
    def verify(input_key: KeyInfo) -> Validity:
        key_union = DNSSECKeyVerification.__cache.get(input_key.email)
        if key_union is not None:
            return DNSSECKeyVerification.__cache_hit(key_union, input_key.key)
        else:
            result = DNSSECKeyVerification.__cache_miss(input_key)
            if result == Validity.VALID:
                DNSSECKeyVerification.__cache[input_key.email] = input_key.key
            elif result == Validity.PROVEN_NONEXISTENCE:
                DNSSECKeyVerification.__cache[input_key.email] = NoKey()
            return result


def nice_user_msg(ki: KeyInfo, v: Validity) -> str:
    prefix = "DNSSEC extension: Key for user " + ki.email + " "
    if v == Validity.VALID:
        return prefix + "is valid."
    else:
        return prefix + "has unknown status."


def any_msg(m: str) -> str:
    return "DNSSEC extension: " + m


class RpmImportedKeys:
    def __init__(self):
        self.pkg_names = RpmImportedKeys.__load_package_list()
        self.keys = RpmImportedKeys.__pkgs_list_into_keys(self.pkg_names)

    @staticmethod
    def __load_package_list() -> List[str]:
        p1 = subprocess.Popen(["rpm", "-q", "gpg-pubkey"], stdout=subprocess.PIPE)
        out = p1.communicate()[0]
        keys = out.decode().split('\n')
        return [x for x in keys if x.startswith('gpg-pubkey')]

    @staticmethod
    def __pkg_name_into_key(pkg) -> KeyInfo:
        # Load output of the rpm -qi call
        p1 = subprocess.Popen(["rpm", "-qi", pkg], stdout=subprocess.PIPE)
        info = p1.communicate()[0].decode().split('\n')
        # Parse packager email
        packager = [x for x in info if x.startswith('Packager')][0]
        email = re.search('<(.*@.*)>', packager).group(1)
        # Parse gpg key
        pgp_start = [n for n, l in enumerate(info) if l.startswith('-----BEGIN PGP PUBLIC KEY BLOCK-----')][0]
        pgp_stop = [n for n, l in enumerate(info) if l.startswith('-----END PGP PUBLIC KEY BLOCK-----')][0]
        pgp_key_lines = list(info[pgp_start + 2:pgp_stop - 1])
        pgp_key_str = ''.join(pgp_key_lines)
        return KeyInfo(email, pgp_key_str.encode('ascii'))

    @staticmethod
    def __pkgs_list_into_keys(packages: List[str]) -> List[KeyInfo]:
        return [RpmImportedKeys.__pkg_name_into_key(x) for x in packages]
