from typing import Union, Dict, List
from enum import Enum
import unbound
import hashlib
import base64
import re

KEYS = ['alg', 'hash', 'ts', 'val']
ctx = unbound.ub_ctx()
ctx.config("/vagrant/unbound/libunbound.conf")
ctx.add_ta_file("/vagrant/root-server/root.zone.signed")
status, result = ctx.resolve('repomd.example.com', unbound.RR_TYPE_TXT, unbound.RR_CLASS_IN)
if status != 0:
    print("error communicating with DNS server")
else:
    data = result.data.as_raw_data()
    structured_result = {}
    for d in data:
        key_val = d.decode('ascii')
        # print(key_val)
        key, val = key_val.split('=')
        print(key, val)

        for k in KEYS:
            if key.endswith(k):
                structured_result[k] = val

    print(structured_result)