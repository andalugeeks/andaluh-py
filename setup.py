#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4
###
#
# Copyright (c) 2018-2020 Andalugeeks
# Authors:
# - Ksar Feui <a.moreno.losana@gmail.com>
# - J. Félix Ontañón <felixonta@gmail.com>
# - Sergio Soto <scots4ever@gmail.com>


from setuptools import setup
# read the contents of your README file
from os import path
import io
THIS_DIRECTORY = path.abspath(path.dirname(__file__))
with io.open(path.join(THIS_DIRECTORY, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='andaluh',
    version='0.2.1',
    description='Transliterate español (spanish) spelling to andaluz proposals',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='J. Félix Ontañón',
    author_email='felixonta@gmail.com',
    url='https://andaluh.es',
    project_urls={
        "Source Code": "https://github.com/andalugeeks/andaluh-py"
    },
    python_requires=">=3.5.*",
    platforms=['win32', 'linux2'],
    license='GNU LESSER GENERAL PUBLIC LICENSE',
    classifiers=[
        "Topic :: Text Processing",
        "Topic :: Software Development :: Internationalization",
        "Natural Language :: Spanish",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    packages=['andaluh'],
    package_dir={'andaluh': 'andaluh'},
    scripts=['bin/andaluh']
)
