.PHONY: build download

build:
	./env/bin/python setup.py install
	./env/bin/mkdocs build

docs/wavedrom.unpkg.js:
	wget -O $@ https://cdn.jsdelivr.net/npm/wavedrom@3.1.0/wavedrom.unpkg.js

docs/skin-default.js:
	wget -O $@ https://wavedrom.com/skins/default.js

download: docs/wavedrom.unpkg.js docs/skin-default.js
	echo

