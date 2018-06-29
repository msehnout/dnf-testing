#!/usr/bin/fish

pushd build
cmake .. -DPYTHON_DESIRED="3"
make
popd
set PYTHONPATH (readlink -f .); bin/dnf-3 clean all
set PYTHONPATH (readlink -f .); coverage3 run bin/dnf-3 --repo=diploma-thesis install test-good-sig -y -d9
set PYTHONPATH (readlink -f .); bin/dnf-3 --repo=diploma-thesis remove test-good-sig -y -d9
rpm -e gpg-pubkey-59e08e43-5a96cdec
