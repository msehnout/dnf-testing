all:
	gcc main.c ${CFLAGS} -o test-good-sig

install:
	mkdir -p ${DESTDIR}/usr/bin
	install -m 0644 test-good-sig ${DESTDIR}/usr/bin/test-good-sig
