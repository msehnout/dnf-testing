pushd root-server
dnssec-signzone -A -N INCREMENT -o . -t root.zone
popd
pushd com-server
dnssec-signzone -A -N INCREMENT -o com. -t com.zone
popd
pushd example-com-server
dnssec-signzone -A -N INCREMENT -o example.com. -t example.com.zone
popd
