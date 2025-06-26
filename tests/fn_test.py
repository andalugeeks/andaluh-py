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

import csv
import pprint
import pytest

import andaluh

# Test cases fixture
@pytest.fixture(params=[
    ('Todo Xenomorfo dice: [haber], que el Éxito y el éxtasis asfixian, si no eres un xilófono Chungo.',
     'Tó Çenomorfo diçe: [abêh], que el Éççito y el éttaçî âffîççian, çi no erê un çilófono Xungo.'),
    ('Lleva un Guijarrito el ABuelo, ¡Qué Bueno! ¡para la VERGÜENZA!',
     'Yeba un Giharrito el AGuelo, ¡Qué Gueno! ¡pa la BERGUENÇA!'),
    ('VALLA valla, si vas toda de ENVIDIA',
     'BAYA baya, çi bâ toa de EMBIDIA'),
    ('Alrededor de la Alpaca había un ALfabeto ALTIVO de valkirias malnacidas',
     'Arrededôh de la Arpaca abía un ARfabeto ARTIBO de barkiriâ mânnaçidâ'),
    ('En la Zaragoza y el Japón asexual se Sabía SÉriamente sILBAR con el COxis',
     'En la Çaragoça y er Hapón açêççuâh çe Çabía ÇÉriamente çIRBÂH con er CÔççî'),
    ('Transportandonos a la connotación perspicaz del abstracto solsticio de Alaska, el aislante plástico adsorvente asfixió al aMnésico pseudoescritor granadino de constituciones, para ConMemorar broncas adscritas',
     'Trâpportandonô a la cônnotaçión perppicâh del âttrâtto çorttiçio de Alâkka, el aîl-lante pláttico âççorbente âffîççió al ânnéçico çeudoêccritôh granadino de côttituçionê, pa CôMMemorâh broncâ âccritâ'),
    ('Venid todos a correr en anorak de visón a Cádiz con actitud y maldad, para escuchar el tríceps de Albéniz tocar ápud con virtud de laúd.',
     'Benîh tôh a corrêh en anorâh de biçón a Cádî con âttitûh y mardá, pa êccuxâh er tríçê de Arbénî tocâh ápû con birtûh de laûh.'),
    ('Una comida fabada con fado, y sin descuido será casada y amarrada al acolchado roido.',
     'Una comida fabada con fado, y çin dêccuido çerá caçá y amarrá al acorxao roío.'),
    ('Los SABuesos ChiHuaHUA comían cacaHuETes, FramBuESas y Heno, ¡y HABLAN con hálito de ESPANGLISH!',
     'Lô ÇAGueçô XiGuaGUA comían cacaGuETê, FramBuEÇâ y Eno, ¡y ABLAN con álito de ÊPPANGLÎ!'),
])
def test_case(request):
    return request.param

# Test cases with special parameters
@pytest.fixture(params=[
    ('Oye sexy psiquiatra @miguel, la #web HTTPS://andaluh.es/transcriptor no çale en google.es pero çi en http://google.com?utm=13_123.html #porqueseñor',
     'Oye çêççy çiquiatra @miguel, la #web HTTPS://andaluh.es/transcriptor no çale en google.es pero çi en http://google.com?utm=13_123.html #porqueseñor',
     {'escape_links': True}),
])
def test_case_with_params(request):
    return request.param

# Basic transcription tests
def test_andaluh_transcription(test_case):
    """Test basic andaluh transcription cases"""
    input_text, expected_output = test_case
    result = andaluh.epa(input_text)
    assert result == expected_output, f"Input: {input_text}\nExpected: {expected_output}\nGot: {result}"

# Transcription tests with parameters
def test_andaluh_transcription_with_params(test_case_with_params):
    """Test andaluh transcription cases with special parameters"""
    input_text, expected_output, params = test_case_with_params
    result = andaluh.epa(input_text, **params)
    assert result == expected_output, f"Input: {input_text}\nExpected: {expected_output}\nGot: {result}"

