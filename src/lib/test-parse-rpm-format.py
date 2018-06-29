from dnsseckeyverification import *
import gnupg
import re

#gpg = gnupg.GPG(gnupghome='/keyring', keyring='pubring.kbx', gpgbinary='gpg2')

#gpg_data_b64 = base64.b64encode(gpg.export_keys(keyids=['C2929F5559E08E43'], armor=False))
#print(gpg_data_b64)

user = 'RPM Packager (The guy who creates packages) <packager@example.com>'
raw_key = b'-----BEGIN PGP PUBLIC KEY BLOCK-----\n\nmQENBFqWzewBCADMHY8wL2Gm+aeShboOfG96/h/OJ8FHj+xrihPGY34FwLVqtvO+\nlRIO6t3w5y7O1MWzR1ePtQg1T1sg1s9UeoDRMZoVgzZdRXtQH1Jy9xpTeMfL31ml\nc3wOnitcH0AdWhT7xnnlaCeJuMrX82PWtiJNd+Cy+bgyLfLMwX18cimwYCnyIHQ5\n4qiiywXa1paVHkbEJdbd8f4AxArsHX33xCv76wct2uXiHYAHu67rE5FhQ0mEqfIZ\nHwuFljGPj5UMgyd6MRMuL2Ho1hL7FDPIxDBv5tMWeZJszixIsCkA9Kc1ibylDz9I\nx/keH1K9XXSb/o2EIfF6sWYcj0wNvJllIHAfABEBAAG0QlJQTSBQYWNrYWdlciAo\nVGhlIGd1eSB3aG8gY3JlYXRlcyBwYWNrYWdlcykgPHBhY2thZ2VyQGV4YW1wbGUu\nY29tPokBTgQTAQgAOBYhBMwU+9636QKkbYsjdMKSn1VZ4I5DBQJals3sAhsDBQsJ\nCAcCBhUKCQgLAgQWAgMBAh4BAheAAAoJEMKSn1VZ4I5D6icH/2GY2MMnmcDO+ApI\nF6gGg9itzAHLTNcxEMl9ht1Gu3JQ/VdsvMQ6lG+U8yffEmsfQebtt1UaMVXzyt0t\ncSOBJvVEI6qc6skvfea3hqL4srtTOCwu7ZBA9gOE+eB5BWBspFUVIwUO1GKT48uz\nV6CaODLitaxc7NrJ9HYw4C4+ICCfbIJhjM/HqxLKOqVy/jsySqIHK96RrjY/m8Q9\nBzsi/6fj/GHkewaM8zaeNLHE7MgXFZAuJ8lzjD0r2oBDJGeBKfjjz9xh26YWjG/A\noiolXfliTEox6p0bf820eRhdX9UdSesBROL3rkB+hM5FOT8crSPJsuGZWJ9brikf\nsurWyU+5AQ0EWpbN7AEIAK0/PThuvsLdDGe5HeZn3VdrFcD9QSOV9Xjos8zWkwx8\nv0t4KXPM4GshyU2ddNjgA+00LhzjACm2ropT5vdvKPtf8lRGOcWWHkiMPdDW/R3/\nI5S0Oh1WFNrQZwQSXn/DoPnhUZNGErpZlUzF00BEltwoVWgT1n81Bp486U3oziZn\nUM8kxXXY2PN8aTfWjsxOSmjyu2m7abeyjTqX9s++vUCQhmCNboSY1AhXF8GQl1Ce\nmpHVv0hOuC6BeadZRXEfEF0sQogswXpFhYG4GFUvVzKBn00/5phNWHvff1GDjzZz\nmVcRPje+rH6gGP8tpQn7NL1SvrazSqSOih//FfV73EMAEQEAAYkBNgQYAQgAIBYh\nBMwU+9636QKkbYsjdMKSn1VZ4I5DBQJals3sAhsMAAoJEMKSn1VZ4I5DshgIALSn\nLy7KL0bcqxoiEZT+P9O+gX34J2NEfITlu3MZyN26LbyJS7HuN1vmuUc/UM0ff7AW\n6eElCNFr5HQOrFELUZWiX7f4U8ihRN39g1PKRGANlUcLm1Z/JnKyYbyzRK70o5A3\n5EiXEHwY62c/b8I1N4kzNKpa0eQcJ7F8XoZhau0UsxqueVPeEIaHX+fjbalz67ea\niFTu8MurdGKntVE1dOPYbGvZE0+HxfDOoVo05bRUH8By7dDgVaI9EijrVzjA5jHP\nJxNIj9AQP9W8zst3l3d9v8o0Pw+L4cWzv+aBFakfjKGugs6lA53fB3RCfZ7OrMwC\nBvlTfDigK9X50K6XoP0=\n=6SRV\n-----END PGP PUBLIC KEY BLOCK-----\n'
key = raw_key.decode('ascii').split('\n')

email = re.search('<(.*@.*)>', user)
print(email.group(1))
print("Key:")
print(key)

print(len(key))
start = next(i for i in range(0,len(key)) if key[i] == '-----BEGIN PGP PUBLIC KEY BLOCK-----')
print(start)
stop = next(i for i in range(0,len(key)) if key[i] == '-----END PGP PUBLIC KEY BLOCK-----')
print(stop)
print(key[start+2:stop-1])
cat_key = ''.join(key[start+2:stop-1]).encode('ascii')
print(cat_key)
#print(gpg_data_b64)

keyinfo = KeyInfo.from_rpm_key_object(user, raw_key)
print(str(keyinfo.email))
print(str(keyinfo.key))
