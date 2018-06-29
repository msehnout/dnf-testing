import subprocess
import re
import dnsseckeyverification as ds

a = ds.RpmImportedKeys()
print(a.pkg_names)
print(a.keys)
