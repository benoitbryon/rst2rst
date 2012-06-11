ROOT_DIR=$(PWD)

install:
	cd ${ROOT_DIR}
	mkdir -p lib/buildout
	wget http://svn.zope.org/*checkout*/zc.buildout/tags/1.5.2/bootstrap/bootstrap.py?content-type=text%2Fplain -O lib/buildout/bootstrap.py
	python lib/buildout/bootstrap.py --distribute
	bin/buildout -N

uninstall:
	rm -r ${ROOT_DIR}/bin ${ROOT_DIR}/lib
