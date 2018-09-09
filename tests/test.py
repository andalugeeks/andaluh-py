#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4
###
# 
# Copyright (c) 2018 EPA
# Authors : J. Félix Ontañón <felixonta@gmail.com>

# -*- coding: utf-8 -*- 

# Import package form parent dir https://gist.github.com/JungeAlexander/6ce0a5213f3af56d7369
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

# Now it can be imported :)
import epa

# Let's test
assert epa.cas_to_epa('Haber, que el Éxito asfixia si no eres Chungo.') == u'aber, que el Êççito asfîççia si no eres Xungo.'
assert epa.cas_to_epa('Lleva un Guijarrito, para la VERGÜENZA!') == u'Yeba un Giharrito, para la BERGUENZA!'
assert epa.cas_to_epa('VALLA valla, si vas de ENVIDIA') == u'BAYA baya, si bas de EMBIDIA'
assert epa.cas_to_epa('Alrededor de la Alpaca habia un ALfabeto ALTIVO de almanaques') == u'Arrededor de la Arpaca abia un ARfabeto ARTIBO de armanaques'