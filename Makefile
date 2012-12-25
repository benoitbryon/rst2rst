develop:
	if [ ! -f lib/buildout/bootstrap.py ]; then \
	    mkdir -p lib/buildout; \
	    wget http://svn.zope.org/*checkout*/zc.buildout/tags/1.5.2/bootstrap/bootstrap.py?content-type=text%2Fplain -O lib/buildout/bootstrap.py; \
	    python lib/buildout/bootstrap.py --distribute; \
	fi
	bin/buildout -N

update: develop

uninstall:
	rm -r bin/ lib/

tests:
	bin/nosetests -v --rednose --with-doctest --with-coverage --cover-erase --nocapture --cover-package=rst2rst rst2rst/

release:
	bin/fullrelease
