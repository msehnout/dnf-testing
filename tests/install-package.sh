#!/bin/bash

# Fail on the first error
set -e
# Download dnf sources
pushd /tmp
git clone 'https://github.com/msehnout/dnf-2.7.5-modularity-6.git'
pushd 'dnf-2.7.5-modularity-6'
dnf builddep dnf.spec -y
dnf install make -y
mkdir build
pushd build
cmake .. -DPYTHON_DESIRED="3"
make
popd # build
# Replace resolv.conf with a testing one
mv /etc/resolv.conf /tmp/resolv.conf.backup
echo "nameserver 192.168.99.199" > /etc/resolv.conf
PYTHONPATH=$(readlink -f .) bin/dnf-3 --repo=local-repo install test-good-sig -y
