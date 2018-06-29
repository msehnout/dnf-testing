from dnssecmdverification import *

print(verify_md('repomd.xml'))
print("########### RESULT ^^^^^\n\n\n")
print(verify_md('repomd-changed.xml'))
print("########### RESULT ^^^^^\n\n\n")
