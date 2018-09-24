#!/bin/bash

# rm /etc/resolv.conf
# mv /tmp/resolv.conf.backup /etc/resolv.conf
echo 'nameserver 192.168.99.1' > /etc/resolv.conf
