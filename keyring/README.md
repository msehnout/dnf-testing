# Key ring

## New version

As it turns out, it is not a good idea to use a cutom name for the keyring file, because it is hard to convince `rpm` to use it, so I have a new approach.

```bash
# Run in this directory
export GNUPGHOME="$PWD"
gpg2 --full-gen-key
gpg2 --list-secret-keys
# Export is the same
```

**Don't forget to copy the new key into the appropriate zone and sign the zone again!**

## Old version

In order to store keys in DNS and use them to sign packages, they need to be created first. This can be done using the `gpg` or `gpg2` utility. In general, if you wish to work with different keyring than the default one use this command:
```
$ gpg2 --no-default-keyring --keyring $PWD/<keyring file> <something>
```

In order to create a new key for testing purposes:
```
$ gpg2 --no-default-keyring --keyring $PWD/testing.gpg --full-gen-key
```
and fill in all necessary fields.

Now, it is necessary to export the previously created key for usage in DNS server (in this case Bind):
```
$ gpg2 --no-default-keyring --keyring $PWD/testing.gpg --export-options export-dane --export packager@example.com
```
