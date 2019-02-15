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

setup(name='epa',
    version='0.1',
    description='Translate castellano (español) to EPA andaluz proposal',
    author='J. Félix Ontañón',
    author_email='felixonta@gmail.com',
    url='https://andaluh.es',
    platforms=['win32', 'linux2'],
    license='GNU LESSER GENERAL PUBLIC LICENSE',

    packages = ['epa'],
    package_dir =  {'epa': 'epa'},

    scripts=['bin/cas_to_epa']
)