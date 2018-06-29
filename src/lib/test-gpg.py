import gnupg

gpg = gnupg.GPG(gnupghome='/keyring', keyring='pubring.kbx', gpgbinary='gpg2')
for i in gpg.list_keys():
    print(str(i['keyid']) + " " + str(i['uids']))

print(gpg.export_keys(keyids=['C2929F5559E08E43'], armor=False))