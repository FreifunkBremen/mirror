# Firmware-Mirror

## About

Fireware-Mirror is a simple python application that should make you able to host a mirror of Freifunk firmware images. Its written in python. The application parses a _site.conf_ and get and verifies the _.manifest_, downloads all new and changed images and validates the file checksums. It was created by @corny and @komaflash .

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
* create a directory, taht is accessible via HTTP, so you can add the url to your site.conf later.
* place you site.conf in the same directory as the mirror.py
* run the following command with the URL of an existing mirror:

    python mirror.py -u https://comunityname.freifunk.tld/mirror -s ./site.conf -r /path/to/http/dir


