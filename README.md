# Firmware-Mirror

## About

Firmware-Mirror is a simple python application that should make you able to host a mirror of Freifunk firmware images. It's written in python. The application downloads and parses a _site.conf_ and gets and verifies the _.manifest_. It downloads all new and changed images and validates the file checksums afterwards. It was created by @corny and @komaflash .

The application contains the following modules:
* __mirror.py__: The heart.
* __downloader.py__: Checks HTTP _if-modified-since_ header and downloads files.
* __gluon_manifest.py__: gluon.manifest parser.
* __slpp.py__: Simple lua-python data structures parser [by SirAnthony](https://github.com/SirAnthony/slpp).

## Requirements

* Python 2.7
* [ECDSA Util](https://github.com/tcatm/ecdsautils)

## Usage

To create a new mirror you have to:
* create a directory, that is accessible via HTTP, so you can add the url to your site.conf as mirror later.
* run the following command with the URL of an existing mirror:

    `python mirror.py --url https://comunityname.freifunk.tld/mirror --site-conf https://raw.githubusercontent.com/FreifunkBremen/gluon-site-ffhb/master/site.conf --root /path/to/http/dir`

