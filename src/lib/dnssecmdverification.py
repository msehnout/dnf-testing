from typing import Union, Dict, List
from enum import Enum
import unbound
import hashlib
import base64


def __load_from_dns(repo_url: str) -> Dict[str, str]:
    repo_url = repo_url if repo_url is not None else "repomd.example.com"
    KEYS = ['alg', 'hash', 'ts', 'val']
    ctx = unbound.ub_ctx()
    ctx.config("/vagrant/unbound/libunbound.conf")
    ctx.add_ta_file("/vagrant/root-server/root.zone.signed")
    status, result = ctx.resolve(repo_url, unbound.RR_TYPE_TXT, unbound.RR_CLASS_IN)
    if status != 0:
        print("error communicating with DNS server")
    else:
        data = result.data.as_raw_data()
        structured_result = {}
        for d in data:
            key_val = d.decode('ascii')
            # print(key_val)
            key, val = key_val.split('=')
            #print(key, val)

            for k in KEYS:
                if key.endswith(k):
                    structured_result[k] = val

        print(structured_result)
        return structured_result


class MdVerificationResult(Enum):
    VALID=0,
    INVALID=1,
    ERROR=2


def __hash_local_file(md_file_name: str) -> str:
    with open(md_file_name, 'rb') as f:
        m = hashlib.sha256()
        while True:
            chunk = f.read(2048)
            if chunk:
                m.update(chunk)
            else:
                break

        digest = base64.b16encode(m.digest()).decode('utf-8').lower()
        return digest


def verify_md(md_file_name: str, repo_url: str = None) -> MdVerificationResult:
    dns_dict = __load_from_dns(repo_url)
    hash = __hash_local_file(md_file_name)
    # TODO: forward alg, check timeout, etc.
    if hash == dns_dict['hash']:
        return MdVerificationResult.VALID
    else:
        return MdVerificationResult.ERROR

