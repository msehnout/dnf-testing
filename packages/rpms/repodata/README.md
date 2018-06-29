# How to create detached signatures

As mentioned in the thesis, you can create them using this command:
```
$ gpg2 --local-user repository@example.com --detach-sign --armor repodata/repomd.xml
```
Note also the local user option as it is necessary to override the default key selection.
