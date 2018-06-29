import time
from dnsseckeyverification import *

import gnupg

gpg = gnupg.GPG(gnupghome='/keyring', keyring='pubring.kbx', gpgbinary='gpg2')


def test_key(email, keyid):
    gpg_data_b64 = base64.b64encode(gpg.export_keys(keyids=[keyid], armor=False))

    keyinfo = KeyInfo()
    keyinfo.email = email
    keyinfo.key = gpg_data_b64

    print("User: " + email + "\twith keyid: " + keyid + ",\tstatus: " + str(DNSSECKeyVerification.verify(keyinfo)))
    print("Key:" + str(keyinfo.key))

# start = time.time()
# test_key("joe@notsigned.com", "3AA7161472344430")
# end = time.time()
# print("time elapsed: " + str(end - start))
# start = time.time()
# test_key("revoked@example.com", "9E159145058CE3E6")
# end = time.time()
# print("time elapsed: " + str(end - start))
start = time.time()
test_key("packager@example.com", "C2929F5559E08E43")
end = time.time()
print("time elapsed: " + str(end - start))
