SHELL := /bin/bash
PKGNAME := test-good-sig

archive:
	tar czvf ${PKGNAME}-0.1.0.tar.gz ${PKGNAME}-0.1.0

srpm: archive
	rpmbuild -bs ${PKGNAME}.spec  --define "_sourcedir ${PWD}"

rpm: archive
	rpmbuild -ba ${PKGNAME}.spec  --define "_sourcedir ${PWD}"

copyhere:
	cp "${HOME}/rpmbuild/RPMS/x86_64/${PKGNAME}-0.1.0-1.fc27.x86_64.rpm" .

sign: export GNUPGHOME = ${HOME}/Github/key-verification-library/keyring
sign: rpm copyhere
	rpm --define='%_gpg_name RPM Packager (The guy who creates packages) <packager@example.com>' --addsign *.rpm

clean:
	rm *.tar.gz *.rpm
