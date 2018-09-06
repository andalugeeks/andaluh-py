#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4
###
# 
# Copyright (c) 2018 EPA
# Authors : J. Félix Ontañón <felixonta@gmail.com>

# -*- coding: utf-8 -*- 

from setuptools import setup

setup(name='epa',
    version='0.1',
    description='Translate castellano (español) to EPA andaluz proposal',
    author='J. Félix Ontañón',
    author_email='felixonta@gmail.com',
    url='https://www.facebook.com/pg/ErPrincipitoAndaluh',
    platforms=['win32', 'linux2'],
    license='GNU LESSER GENERAL PUBLIC LICENSE',

    packages = ['epa'],
    package_dir =  {'epa': 'epa'},

    scripts=['bin/cas_to_epa']
)