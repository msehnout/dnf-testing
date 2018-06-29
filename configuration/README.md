# Root DNS server configuration

The named.conf file was taken from some examples. The zone file was written by hand and signed using this sequence:

 1. Generate keys and include them:
```fish
dnssec-keygen -n ZONE .
dnssec-keygen -f KSK -n ZONE .
# where . stands for the domain name
for i in *.key
echo "\$INCLUDE" $i >> root.zone 
end
```
This process is the same for all zones.

 2. Sign child zones, e.g. for `com.` zone:
```fish
dnssec-signzone -A -N INCREMENT -o com. -t com.zone
```
 
 3. Append dsset-`zone` file content to the parent zone file and sign the parent zone
```fish
cat ../com-server/dsset-com. >> root.zone
```

 4. Add root zone KSK to the manages keys list of the resolver
```fish
cat root-server/K.+005+20617.key 
; This is a key-signing key, keyid 20617, for .
; Created: 20180216121340 (Fri Feb 16 13:13:40 2018)
; Publish: 20180216121340 (Fri Feb 16 13:13:40 2018)
; Activate: 20180216121340 (Fri Feb 16 13:13:40 2018)
. IN DNSKEY 257 3 5 AwEAAbDej270bMAPIIEQJdEg6FqTNiTqxqbnAGNLsv4kdiVblL5C4bjv p1hp+fdjZi5Teqsa90ORbNqjG4ZoA1HO2XKEdpfRwrg/2UiCoVZljKwq 6Rw8yx4fgb4FiE2Kz2Uwiva3NnHRyKAplOXBSo22LaqXoTRjibzsAqYn DTOKIvwZBIKETRMmpt5TLIkscXj4kZVjqo9inDqE5yZf6ZyPgxJLQh1u Uez7gFTFztM3WKli77+imRfoMmf32yawbaB9iTC0n9Iwac5aiL/IHZd8 tJc226wPVMt9VFUb+cWqPbogyMiA27o19fisFwnUYdUdSB5knglXA6aI uo9ynW6rbks=
```
and insert it to the configuration file:
```
managed-keys {
"." initial-key 257 3 5 "AwEAAbDej270bMAPIIEQJdEg6FqTNiTqxqbnAGNLsv4kdiVblL5C4bjv p1hp+fdjZi5Teqsa90ORbNqjG4ZoA1HO2XKEdpfRwrg/2UiCoVZljKwq 6Rw8yx4fgb4FiE2Kz2Uwiva3NnHRyKAplOXBSo22LaqXoTRjibzsAqYn DTOKIvwZBIKETRMmpt5TLIkscXj4kZVjqo9inDqE5yZf6ZyPgxJLQh1u Uez7gFTFztM3WKli77+imRfoMmf32yawbaB9iTC0n9Iwac5aiL/IHZd8 tJc226wPVMt9VFUb+cWqPbogyMiA27o19fisFwnUYdUdSB5knglXA6aI uo9ynW6rbks=";
};
```
