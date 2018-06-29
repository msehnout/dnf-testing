import unbound
import base64
import gnupg

import dnslocation
from dnslocation import email2location

print("Unbound resolver test:")

ctx = unbound.ub_ctx()
#ctx.resolvconf("/tmp/resolv.conf")
ctx.config("/vagrant/unbound/libunbound.conf")
ctx.add_ta_file("/vagrant/root-server/root.zone.signed")


def print_result(status, result):
    if status == 0 and result.havedata:
        print("Result:", result.data)
        if result.secure:
            print("Result is secure")
        elif result.bogus:
            print("Result is bogus")
        else:
            print("Result is insecure")


status, result = ctx.resolve("notsigned.com")
#print_result(*ctx.resolve("d6fb116e0485a16e447de0c6317eb48e6ce1370e7986400f95ebad00._openpgpkey.example.com.", 61, unbound.RR_CLASS_IN))

status, result = ctx.resolve(email2location("packager@example.com"),
                             61, unbound.RR_CLASS_IN)
if status == 0 and result.havedata:
    data = result.data.as_raw_data()[0]
    print("data:")
    dns_data_b64 = base64.b64encode(data)
    print(dns_data_b64)
    gpg = gnupg.GPG(gnupghome='/keyring', keyring='testing.gpg', gpgbinary='gpg2')
    gpg.list_keys()
    gpg_data_b64 = base64.b64encode(gpg.export_keys(keyids=['1E9893670B36418B'], armor=False))
    print(gpg_data_b64)
    if dns_data_b64 == gpg_data_b64:
        print("MATCH")
    else:
        print("FAIL")


status, result = ctx.resolve(email2location("revoked@example.com"),
                             61, unbound.RR_CLASS_IN)
if status == 0 and result.havedata:
    data = result.data.as_raw_data()[0]
    print("data:")
    dns_data_b64 = base64.b64encode(data)
    print(dns_data_b64)
    gpg = gnupg.GPG(gnupghome='/keyring', keyring='testing.gpg', gpgbinary='gpg2')
    gpg.list_keys()
    gpg_data_b64 = base64.b64encode(gpg.export_keys(keyids=['0D09386D166D926C'], armor=False))
    print(gpg_data_b64)
    if dns_data_b64 == gpg_data_b64:
        print("VALID")
    else:
        print("REVOKED")


def print_result_structure(status, result, email):
    print("[###] Status(" + email + "): " + str(status) + ", bogus: " + str(result.bogus)
          + ", havedata: " + str(result.havedata)
          + ", nxdomain: " + str(result.nxdomain)
          + ", secure: " + str(result.secure)
          + ", why_bogus: " + str(result.why_bogus)
          )


def query_email(email):
    print_result_structure(*ctx.resolve(email2location(email),
                                        61, unbound.RR_CLASS_IN), email)


emails = ["packager@example.com", "revoked@example.com", "non-existing-key@example.com", "test@non-existing-domain.com", "non-existing@wrongconfig.com",
          "joe@notsigned.com"]
for e in emails:
    query_email(e)

