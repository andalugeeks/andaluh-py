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

# Basic tests
def test1():
    assert epa.cas_to_epa('Xenomorfo dice: [haber], que el Éxito y el éxtasis asfixian, si no eres un xilófono Chungo.') == u'Çenomorfo diçe: [abêh], que el Éççito y el éttaçî âffîççian, çi no erê un çilófono Xungo.'
    assert epa.cas_to_epa('Lleva un Guijarrito, para la VERGÜENZA!') == u'Yeba un Giharrito, para la BERGUENÇA!'
    assert epa.cas_to_epa('VALLA valla, si vas de ENVIDIA') == u'BAYA baya, çi bâ de EMBIDIA'
    assert epa.cas_to_epa('Alrededor de la Alpaca había un ALfabeto ALTIVO de valkirias malnacidas') == u'Arrededôh de la Arpaca abía un ARfabeto ARTIBO de barkiriâ mânnaçidâ'
    assert epa.cas_to_epa('En la Zaragoza asexual se Sabía SÉriamente sILBAR con el COxis') == u'En la Çaragoça açêççuâh çe Çabía ÇÉriamente çIRBÂH con el CÔççî'
    assert epa.cas_to_epa('Transportandonos a la connotación perspicaz del abstracto solsticio de Alaska, el aislante plástico adsorvente asfixió al aMnésico pseudoescritor granadino de constituciones, para ConMemorar broncas adscritas') == u'Trâpportandonô a la cônnotaçión perppicâh dêh âttrâtto çorttiçio de Alâkka, el aîl-lante pláttico âççorbente âffîççió al ânnéçico çeudoêccritôh granadino de côttituçionê, para CôMMemorâh broncâ âccritâ'
    assert epa.cas_to_epa('En la postmodernidad, el transcurso de los transportes y translados en postoperatorios transcienden a la postre unas postillas postpalatales apostilladas se transfieren') == u'En la pômmodênnidá, el trâccurço de lô trâpportê y trâl-ladô en pôttoperatoriô trâççienden a la pôttre unâ pôttiyâ pôppalatalê apôttiyadâ çe trâffieren'
    assert epa.cas_to_epa('Venid a correr en anorak a Cádiz con actitud y maldad, para escuchar el tríceps de Albéniz tocar ápud con virtud de laúd.') == u'Benîh a corrêh en anorâh a Cádî con âttitûh y mardá, para êccuxâh el tríçê de Arbénî tocâh ápû con birtûh de laûh.'
    assert epa.cas_to_epa('Una comida fabada con fado, y sin descuido será casada y amarrada al acolchado roido.') == u'Una comida fabada con fado, y çin dêccuido çerá caçá y amarrá al acorxao roío.'

# Lemario test
def test2(report_all = False):

    import csv
    file = "./tests/lemario_cas_and.csv"

    transcriptions = []
    transcription_errors = []
    stats = {"total": 0, "ok": 0, "fail": 0}

    with open(file) as fh:
        rd = csv.DictReader(fh, delimiter=',')

        for row in rd:
            caste = unicode(row['cas'], 'utf-8')
            andal = unicode(row['and'], 'utf-8')
            trans = epa.cas_to_epa(row['cas'])

            if andal != trans:
                transcription_errors.append((caste, andal, trans))
                stats["fail"] += 1
            else:
                stats["ok"] += 1

            transcriptions.append((caste, andal, trans))
            stats["total"] += 1
    

    if report_all:
        for error in transcription_errors:
            print error[0] + " => " + error[1] + ', ' + error[2]
    import pprint
    pprint.pprint(stats)

if __name__ == '__main__':
    test1()
    test2(True)