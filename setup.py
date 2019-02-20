#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4
###
# 
# Copyright (c) 2018-2019 Andalugeeks
# Authors:
# - Ksar Feui <a.moreno.losana@gmail.com>
# - J. Félix Ontañón <felixonta@gmail.com>

# -*- coding: utf-8 -*- 

from setuptools import setup

setup(name='andaluh',
    version='0.1.0',
    description='Transliterate castellano (español) spelling to andaluz proposals',
    author='J. Félix Ontañón',
    author_email='felixonta@gmail.com',
    url='https://andaluh.es',
    platforms=['win32', 'linux2'],
    license='GNU LESSER GENERAL PUBLIC LICENSE',

    packages = ['andaluh'],
    package_dir =  {'andaluh': 'andaluh'},

    scripts=['bin/andaluh']
)