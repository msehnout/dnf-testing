# Testing environment for DNSSEC extension

Setup should be as easy as:
```
vagrant up
```
This will spin up both server and client. Then you can log in to the client machine
```
vagrant ssh client
```
and run the test in `/tests` directory
```
cd /tests
bash <test>
```
