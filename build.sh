#!/bin/bash

rm -rf venv
virtualenv venv

source venv/bin/activate

#pip3 uninstall crypto
#pip3 uninstall pycrypto
#pip3 install pycryptodome
#pip install http://libguestfs.org/download/python/guestfs-1.40.2.tar.gz

pyinstaller -F main.py -n image_maker

deactivate

rm -rf build
