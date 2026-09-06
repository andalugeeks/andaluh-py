#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Tests unitarios para la función transformar_preposicion_en
"""

import pytest
from andaluh import transformar_preposicion_en


@pytest.mark.parametrize("input_text, expected_output", [
    # 1. Regla de prioridad en + el -> n'el (y n'er)
    ("está en el avión", "está n'el avión"),
    ("ocurrió en el altillo", "ocurrió n'el altillo"),
    ("en el coche", "n'el coche"),
    ("vivir en el campo", "vivir n'el campo"),
    ("dormir en el suelo", "dormir n'el suelo"),
    ("en er campo", "n'er campo"),
    # Mayúsculas / TitleCase
    ("En el avión", "N'el avión"),
    ("En el coche", "N'el coche"),
    ("EN EL AVIÓN", "N'EL AVIÓN"),
    ("EN EL COCHE", "N'EL COCHE"),
    ("EN ER CAMPO", "N'ER CAMPO"),
])
def test_preposicion_en_con_el(input_text, expected_output):
    assert transformar_preposicion_en(input_text) == expected_output


@pytest.mark.parametrize("input_text, expected_output", [
    # 2. Regla 'n (Vocal a, e, o anterior + Consonante posterior)
    ("iré en cinco", "iré 'n cinco"),
    ("estará en Granada", "estará 'n Granada"),
    ("sentarse en la silla", "sentarse 'n la silla"),
    ("vino en tren", "vino 'n tren"),
    ("casa en ruinas", "casa 'n ruinas"),
    ("dejó en ridículo", "dejó 'n ridículo"),
    ("pásate en primavera", "pásate 'n primavera"),
    # Mayúsculas
    ("IRÉ EN CINCO", "IRÉ 'N CINCO"),
    ("ESTARÁ EN GRANADA", "ESTARÁ 'N GRANADA"),
])
def test_preposicion_en_vocal_aeo_consonante(input_text, expected_output):
    assert transformar_preposicion_en(input_text) == expected_output


@pytest.mark.parametrize("input_text, expected_output", [
    # 3. Casos no modificados
    # Precedido por vocal 'i' o 'u'
    ("salí en tren", "salí en tren"),
    ("escribí en secreto", "escribí en secreto"),
    ("un iglú en Madrid", "un iglú en Madrid"),
    # Precedido por consonante
    ("árbol en flor", "árbol en flor"),
    ("por en medio", "por en medio"),
    ("comer en paz", "comer en paz"),
    ("vienen en tren", "vienen en tren"),
    ("tienen en cuenta", "tienen en cuenta"),
    # Inicio de frase con consonante posterior (no seguido de 'el')
    ("En cinco minutos", "En cinco minutos"),
    ("En Granada llueve", "En Granada llueve"),
    # Seguido de vocal (distinta de 'el')
    ("creer en algo", "creer en algo"),
    ("vivir en armonía", "vivir en armonía"),
    ("estar en enero", "estar en enero"),
])
def test_preposicion_en_no_modificado(input_text, expected_output):
    assert transformar_preposicion_en(input_text) == expected_output


@pytest.mark.parametrize("input_text, expected_output", [
    # 4. Falsos positivos en subcadenas
    ("entrar en casa", "entrar en casa"),
    ("encima de todo", "encima de todo"),
    ("enano", "enano"),
    ("puente", "puente"),
])
def test_evitar_falsos_positivos_en(input_text, expected_output):
    assert transformar_preposicion_en(input_text) == expected_output


@pytest.mark.parametrize("input_text, expected_output", [
    # 5. Puntuación y casos borde
    ("¡En el avión!", "¡N'el avión!"),
    ("¿En el coche?", "¿N'el coche?"),
    ("Hola, en cinco minutos", "Hola, en cinco minutos"),
    (
        "Iré en tren y dormiré en el hotel",
        "Iré 'n tren y dormiré n'el hotel"
    ),
    ("", ""),
    ("Pensar en", "Pensar en"),
])
def test_puntuacion_y_casos_borde_en(input_text, expected_output):
    assert transformar_preposicion_en(input_text) == expected_output
