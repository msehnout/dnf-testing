import hashlib
import base64
import json

with open('repomd.xml', 'rb') as f:
    m = hashlib.sha256()
    while True:
        chunk = f.read(2048)
        if chunk:
            m.update(chunk)
        else:
            break

    digest = base64.b16encode(m.digest()).decode('utf-8').lower()
    print("; " + digest + " <- digest")

    output_rr = {
        'alg': 'sha256',
        'hash': digest,
        'ts': '24/03/2018',
        'val': '9d'
    }
    dump = json.dumps(output_rr)
    print("; " + dump)

    print("$ORIGIN repomd.example.com.")
    print("@ IN TXT alg=sha256")
    print("@ IN TXT hash=" + digest + "")
    print("@ IN TXT ts=24/03/2018")
    print("@ IN TXT val=9d")
