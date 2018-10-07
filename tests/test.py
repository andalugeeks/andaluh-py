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
assert epa.cas_to_epa('Xenomorfo dice: [haber], que el Éxito asfixia si no eres un xilófono Chungo.') == u'Çenomorfo diçe: [abêh], que el Éççito âffîççia çi no erê un çilófono Xungo.'
assert epa.cas_to_epa('Lleva un Guijarrito, para la VERGÜENZA!') == u'Yeba un Giharrito, para la BERGUENÇA!'
assert epa.cas_to_epa('VALLA valla, si vas de ENVIDIA') == u'BAYA baya, çi bâ de EMBIDIA'
assert epa.cas_to_epa('Alrededor de la Alpaca había un ALfabeto ALTIVO de almanaques') == u'Arrededôh de la Arpaca abía un ARfabeto ARTIBO de armanaquê'
assert epa.cas_to_epa('En Zaragoza se Sabía SÉriamente sILBAR') == u'En Çaragoça çe Çabía ÇÉriamente çIRBÂH'
assert epa.cas_to_epa('Transportandonos al abstracto solsticio, el plástico aislante asfixió al pseudoescritor con aMNesia para ConMemorar broncas') == u'Trâpportandonô al âttrâtto çorttiçio, el pláttico aîl-lante âffîççió al çeudoêccritôh con âNNeçia para CoMMemorâh broncâ'
assert epa.cas_to_epa('Venid a correr en Cádiz con actitud y maldad, para escuchar a Albéniz tocar ápud con virtud de laúd.') == u'Benîh a corrêh en Cádî con âttitûh y mardá, para êccuxâh a Arbénî tocâh ápû con birtûh de laúd.'