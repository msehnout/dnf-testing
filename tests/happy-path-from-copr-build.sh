#!/bin/bash

# Fail on the first error
set -e
# Download dnf sources
DIRNAME='dnf'
PKGNAME='test-good-sig'
KEYNAME='gpg-pubkey-59e08e43-5a96cdec'
test -f '/etc/yum.repos.d/_copr_mblaha-dnf.repo' || dnf copr enable mblaha/dnf
rpm -q dnf | grep git || dnf --best --allowerasing update dnf
# Replace resolv.conf with a testing one
mv /etc/resolv.conf /tmp/resolv.conf.backup
echo "nameserver 192.168.99.199" > /etc/resolv.conf
rpm -q "${KEYNAME}"  && rpm -e "${KEYNAME}"
rpm -q "${PKGNAME}" && dnf remove "${PKGNAME}" -y
echo 'gpgkey_dns_verification=True' >> /etc/dnf/dnf.conf
dnf --repo=local-repo install "${PKGNAME}" -y
