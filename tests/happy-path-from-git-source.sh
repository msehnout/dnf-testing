#!/bin/bash

# Fail on the first error
set -e
# Download dnf sources
pushd /tmp
DIRNAME='dnf'
PKGNAME='test-good-sig'
KEYNAME='gpg-pubkey-59e08e43-5a96cdec'
if [ ! -d "${DIRNAME}" ]; then
    git clone "https://github.com/msehnout/${DIRNAME}"
    pushd "${DIRNAME}"
    dnf builddep dnf.spec -y
    dnf install make -y
    mkdir build
    pushd build
    cmake .. -DPYTHON_DESIRED="3"
    make
    popd # build
else
    pushd "${DIRNAME}"
fi
# Replace resolv.conf with a testing one
mv /etc/resolv.conf /tmp/resolv.conf.backup
echo "nameserver 192.168.99.199" > /etc/resolv.conf
rpm -q "${KEYNAME}"  && rpm -e "${KEYNAME}"
rpm -q "${PKGNAME}" && dnf remove "${PKGNAME}"
PYTHONPATH=$(readlink -f .) bin/dnf-3 --repo=local-repo install "${PKGNAME}" -y
