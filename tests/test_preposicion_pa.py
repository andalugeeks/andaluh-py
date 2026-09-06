#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Tests unitarios para la función transformar_preposicion_pa
"""

import pytest
from andaluh import transformar_preposicion_pa


@pytest.mark.parametrize("input_text, expected_output", [
    # Regla p': pa + 'a' / 'á' / 'â' -> p'a...
    ("pa abajo", "p'abajo"),
    ("pa almorzâ", "p'almorzâ"),
    ("pa arriba", "p'arriba"),
    ("pa acá", "p'acá"),
    ("pa aquel", "p'aquel"),
    ("pa allá", "p'allá"),
    ("pa adelante", "p'adelante"),
    ("pa afuera", "p'afuera"),
    ("pa árboles", "p'árboles"),
    ("pa ámbito", "p'ámbito"),
    ("pa âccedêh", "p'âccedêh"),
    ("pa âttitûh", "p'âttitûh"),
    # Mayúsculas / TitleCase
    ("Pa abajo", "P'abajo"),
    ("Pa allá", "P'allá"),
    ("PA ABAJO", "P'ABAJO"),
    ("VAMOS PA ARRIBA", "VAMOS P'ARRIBA"),
])
def test_regla_pa_vocal_a_posterior(input_text, expected_output):
    assert transformar_preposicion_pa(input_text) == expected_output


@pytest.mark.parametrize("input_text, expected_output", [
    # Otras vocales (e, i, o, u) - no se transforman
    ("pa ellos", "pa ellos"),
    ("pa este", "pa este"),
    ("pa ir", "pa ir"),
    ("pa otro", "pa otro"),
    ("pa usted", "pa usted"),
    ("pa uno", "pa uno"),
    # Consonantes - no se transforman
    ("pa ti", "pa ti"),
    ("pa mí", "pa mí"),
    ("pa comer", "pa comer"),
    ("pa siempre", "pa siempre"),
    ("pa qué", "pa qué"),
    ("Pa nada", "Pa nada"),
    ("PA TODOS", "PA TODOS"),
])
def test_regla_pa_otras_letras_no_modificadas(input_text, expected_output):
    assert transformar_preposicion_pa(input_text) == expected_output


@pytest.mark.parametrize("input_text, expected_output", [
    # Palabras que contienen 'pa' pero no son la preposición aislada
    ("para abajo", "para abajo"),
    ("papel de regalo", "papel de regalo"),
    ("pala ancha", "pala ancha"),
    ("capa azul", "capa azul"),
    ("copa alta", "copa alta"),
    ("padrino", "padrino"),
    ("pasa pa allá", "pasa p'allá"),
])
def test_evitar_falsos_positivos_subcadenas_pa(input_text, expected_output):
    assert transformar_preposicion_pa(input_text) == expected_output


@pytest.mark.parametrize("input_text, expected_output", [
    # Puntuación y casos borde
    ("¡Pa arriba!", "¡P'arriba!"),
    ("¿Pa dónde?", "¿Pa dónde?"),
    ("Hola, pa acordarnos", "Hola, p'acordarnos"),
    (
        "Tira pa adelante y no mires pa atrás",
        "Tira p'adelante y no mires p'atrás"
    ),
    (
        "Un regalo pa Antonio y otro pa Carlos",
        "Un regalo p'Antonio y otro pa Carlos"
    ),
    ("", ""),
    ("Tirando pa", "Tirando pa"),
])
def test_puntuacion_y_casos_borde_pa(input_text, expected_output):
    assert transformar_preposicion_pa(input_text) == expected_output
