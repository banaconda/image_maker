#!/bin/bash

rm -rf venv
virtualenv venv

source venv/bin/activate

#pip install http://libguestfs.org/download/python/guestfs-1.40.2.tar.gz

pyinstaller -F main.py


rm -rf build
