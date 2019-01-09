#!/usr/bin/env python3
#
#
# Copyright (c) 2018, Hiroyuki Ohsaki.
# All rights reserved.
#
# $Id: setup.py,v 1.1 2018/12/20 00:38:09 ohsaki Exp ohsaki $
#

# https://docs.python.org/3.6/distributing/index.html

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# Pytess
setuptools.setup(
    name="pydtnsim",
    version="0.1",
    author="Hiroyuki Ohsaki",
    author_email="ohsaki@lsnl.jp",
    description="A simulator for DTN routing with several agent/mobility models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://www.lsnl.jp/~ohsaki/software/pydtnsim/",
    packages=setuptools.find_packages(),
    scripts=['bin/pydtnsim'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GPL",
        "Operating System :: OS Independent",
    ],
)
