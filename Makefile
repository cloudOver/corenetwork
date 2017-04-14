all:
	echo Nothing to compile

install:
	mkdir -p $(DESTDIR)/etc/corenetwork/
	mkdir -p $(DESTDIR)/etc/sudoers.d/
	cp -r sudoers.cloudover $(DESTDIR)/etc/sudoers.d/corenetwork
	cp -r config/* $(DESTDIR)/etc/corenetwork/
	python setup.py install --root=$(DESTDIR)

egg:
	python setup.py sdist bdist_egg

egg_install:
	python setup.py install

egg_upload:
	# python setup.py sdist bdist_egg upload
	python setup.py sdist upload
egg_clean:
	rm -rf build/ dist/ pyCore.egg-info/ corenetwork.egg-info/
