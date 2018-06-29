BINNAME := test-revoked-key

all:
	gcc main.c ${CFLAGS} -o ${BINNAME}

install:
	mkdir -p ${DESTDIR}/usr/bin
	install -m 0644 ${BINNAME} ${DESTDIR}/usr/bin/${BINNAME}
