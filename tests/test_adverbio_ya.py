#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Tests unitarios para la función transformar_adverbio_ya
"""

import pytest
from andaluh import transformar_adverbio_ya


@pytest.mark.parametrize("input_text, expected_output", [
    # Regla y': ya + 'a' / 'á' / 'â' -> y'a...
    ("ya acaba", "y'acaba"),
    ("ya almorzó", "y'almorzó"),
    ("ya arriba", "y'arriba"),
    ("ya acá", "y'acá"),
    ("ya aquel", "y'aquel"),
    ("ya allá", "y'allá"),
    ("ya adelante", "y'adelante"),
    ("ya afuera", "y'afuera"),
    ("ya árboles", "y'árboles"),
    ("ya ámbito", "y'ámbito"),
    ("ya âccedêh", "y'âccedêh"),
    ("ya âttitûh", "y'âttitûh"),
    # Mayúsculas / TitleCase
    ("Ya acaba", "Y'acaba"),
    ("Ya almorzó", "Y'almorzó"),
    ("YA ACABÓ", "Y'ACABÓ"),
    ("YA ALLÁ", "Y'ALLÁ"),
])
def test_regla_ya_vocal_a_posterior(input_text, expected_output):
    assert transformar_adverbio_ya(input_text) == expected_output


@pytest.mark.parametrize("input_text, expected_output", [
    # Otras vocales (e, i, o, u) - no se transforman
    ("ya está", "ya está"),
    ("ya era", "ya era"),
    ("ya iba", "ya iba"),
    ("ya oigo", "ya oigo"),
    ("ya uso", "ya uso"),
    # Consonantes - no se transforman
    ("ya viene", "ya viene"),
    ("ya sé", "ya sé"),
    ("ya tengo", "ya tengo"),
    ("ya no", "ya no"),
    ("ya podemos", "ya podemos"),
    ("Ya voy", "Ya voy"),
    ("YA VEMOS", "YA VEMOS"),
])
def test_regla_ya_otras_letras_no_modificadas(input_text, expected_output):
    assert transformar_adverbio_ya(input_text) == expected_output


@pytest.mark.parametrize("input_text, expected_output", [
    # Palabras que contienen 'ya' pero no son el adverbio aislado
    ("haya agua", "haya agua"),
    ("vaya allá", "vaya allá"),
    ("playa abierta", "playa abierta"),
    ("yate azul", "yate azul"),
    ("yacimiento", "yacimiento"),
    ("mayo", "mayo"),
])
def test_evitar_falsos_positivos_subcadenas_ya(input_text, expected_output):
    assert transformar_adverbio_ya(input_text) == expected_output


@pytest.mark.parametrize("input_text, expected_output", [
    # Puntuación y casos borde
    ("¡Ya acaba!", "¡Y'acaba!"),
    ("¿Ya abrió?", "¿Y'abrió?"),
    ("Hola, ya hablaremos", "Hola, ya hablaremos"),
    (
        "Si ya acaba, entonces vamos",
        "Si y'acaba, entonces vamos"
    ),
    ("", ""),
    ("Terminado ya", "Terminado ya"),
])
def test_puntuacion_y_casos_borde_ya(input_text, expected_output):
    assert transformar_adverbio_ya(input_text) == expected_output
