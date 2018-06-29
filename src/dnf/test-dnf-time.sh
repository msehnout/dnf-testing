run_test() {
   RESULT=$({ time $1 --repo=diploma-thesis install test-good-sig -y; } 2>&1 | grep '^real')
   printf "${1} ${RESULT}\n"
   rpm -e gpg-pubkey-59e08e43-5a96cdec &> /dev/null
   dnf --repo=diploma-thesis remove test-good-sig -y &> /dev/null
}

COUNT=100

for i in $(seq 1 ${COUNT})
do
   run_test dnf
done

for i in $(seq 1 ${COUNT})
do
   run_test bin/dnf-3
done
