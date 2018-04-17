#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
# To generate DEB package from Python Package:
# sudo pip3 install stdeb
# python3 setup.py --verbose --command-packages=stdeb.command bdist_deb
#
#
# To generate RPM package from Python Package:
# sudo apt-get install rpm
# python3 setup.py bdist_rpm --verbose --fix-python --binary-only
#
#
# To generate EXE MS Windows from Python Package (from MS Windows only):
# python3 setup.py bdist_wininst --verbose
#
#
# To generate PKGBUILD ArchLinux from Python Package (from PyPI only):
# sudo pip3 install git+https://github.com/bluepeppers/pip2arch.git
# pip2arch.py PackageNameHere
#
#
# To Upload to PyPI by executing:
# sudo pip install --upgrade pip setuptools wheel virtualenv
# python3 setup.py bdist_egg bdist_wheel --universal sdist --formats=zip upload --sign


"""Generic Setup.py.
ALL THE CONFIG LIVES IN SETUP.CFG,PLEASE EDIT THERE,KEEP IT SIMPLE AND CLEAN."""


import sys

from setuptools import setup
from shutil import which


if not which("go"):
    print("WARNING: GO not found, please install Go 1.10+.")
    sys.exit(42)

if sys.platform.startswith("win"):
    print("WARNING: Windows is not supported at this time, please install Linux.")
    sys.exit(42)


setup(py_modules=["gothon"])
