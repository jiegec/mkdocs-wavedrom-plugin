mkdocs-wavedrom-plugin
=========================================================

A MkDocs plugin,
render waveform charts in the wavedrom style.

Installation
--------------------------
Install this package with pip.

### from GitHub

```bash
pip install git+https://github.com/jiegec/mkdocs-wavedrom-plugin
```

How to use
--------------------------
More information about plugins in the [MkDocs documentation][mkdocs-plugins]

[mkdocs-plugins]: http://www.mkdocs.org/user-guide/plugins/

### write markdown/wavedrom code

embed your wavedrom code in markdown documents.

<pre>
```wavedrom
{ signal: [{ name: 'Alfa', wave: '01.zx=ud.23.45' }] }
```
</pre>

or see [a sample markdown](https://github.com/jiegec/mkdocs-wavedrom-plugin/blob/main/docs/test.md) for the sample.


### setup mkdocs.yml

change mkdocs.yml to use this plugin.

```yaml
site_name: test
plugins:
    - wavedrom
        embed_svg: false # true if embedding svg in html

extra_javascript:
    # - wavedrom.unpkg.js
    # - skin-default.js
    # above, place *.js in docs directory, or below from internet.
    - https://cdnjs.cloudflare.com/ajax/libs/wavedrom/3.1.0/skins/default.js
    - https://cdnjs.cloudflare.com/ajax/libs/wavedrom/3.1.0/wavedrom.min.js
```


Demo
--------------------------

### from local

```shell
$ python -m venv env
$ ./env/bin/python setup.py install
$ ./env/bin/mkdocs build
$ ./env/bin/mkdocs serve &
$ browse http://localhost:8000/test/index.html
```

or `make build` and `browse site/test/index.html`, if you have make binary.

### (optional) download wavedrom

to download javascript files to local

```shell
$ make download
```

Thanks
--------------------------

a lot part of this plugin were came from mkdocs-mermaid-plugin


<!--
vi: ft=markdown:et:fdm=marker
-->

