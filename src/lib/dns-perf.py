from dnsseckeyverification import DNSSECKeyVerification, KeyInfo

print('Start test')
info = KeyInfo('packager@example.com')
res = DNSSECKeyVerification.verify(info)
print(res)