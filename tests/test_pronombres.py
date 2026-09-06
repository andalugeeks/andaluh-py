#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Tests unitarios para la función transformar_pronombres_atonos
(me, te, se, le, la, lo)
"""

import pytest
from andaluh import transformar_pronombres_atonos


@pytest.mark.parametrize("input_text, expected_output", [
    # 1. Pronombres me, te, se - Vocal posterior general
    ("me abandona", "m'abandona"),
    ("se entra", "s'entra"),
    ("te olvidas", "t'olvidas"),
    ("me imagino", "m'imagino"),
    ("se une", "s'une"),
    ("me alegro", "m'alegro"),
    ("te echo de menos", "t'echo de menos"),
    ("se asombra", "s'asombra"),
    ("me ocurre", "m'ocurre"),
    ("se utiliza", "s'utiliza"),
    # Mayúsculas / TitleCase
    ("Me abandona", "M'abandona"),
    ("Se entra", "S'entra"),
    ("Te olvidas", "T'olvidas"),
    ("ME ABANDONA", "M'ABANDONA"),
    ("SE ENTRA", "S'ENTRA"),
    ("TE OLVIDAS", "T'OLVIDAS"),
])
def test_pronombres_me_te_se_vocal(input_text, expected_output):
    assert transformar_pronombres_atonos(input_text) == expected_output


@pytest.mark.parametrize("input_text, expected_output", [
    # 2. Pronombre 'le' - Cualquier vocal posterior
    ("no le importa", "no l'importa"),
    ("le espera", "l'espera"),
    ("le ayuda", "l'ayuda"),
    ("le ocurre", "l'ocurre"),
    ("le une", "l'une"),
    ("le abre", "l'abre"),
    ("le encantó", "l'encantó"),
    # 'le' seguido de auxiliar antes de consonante
    ("le han dado", "l'han dado"),
    ("le ha dicho", "l'ha dicho"),
    # Mayúsculas
    ("Le importa", "L'importa"),
    ("Le espera", "L'espera"),
    ("LE HAN DADO", "L'HAN DADO"),
])
def test_pronombre_le_vocal(input_text, expected_output):
    assert transformar_pronombres_atonos(input_text) == expected_output


@pytest.mark.parametrize("input_text, expected_output", [
    # 3. Pronombre 'lo' - Vocal 'a' u 'o'
    ("lo ocultó", "l'ocultó"),
    ("lo olvidaron", "l'olvidaron"),
    ("lo agarró", "l'agarró"),
    ("lo agradece", "l'agradece"),
    ("lo odia", "l'odia"),
    ("lo asume", "l'asume"),
    # Mayúsculas
    ("Lo ocultó", "L'ocultó"),
    ("LO OLVIDARON", "L'OLVIDARON"),
    # 'lo' con otras vocales o consonantes (no se modifica)
    ("lo espera", "lo espera"),
    ("lo imagina", "lo imagina"),
    ("lo une", "lo une"),
    ("lo busca", "lo busca"),
    ("lo sabe", "lo sabe"),
    ("Lo tiene", "Lo tiene"),
])
def test_pronombre_lo_vocal(input_text, expected_output):
    assert transformar_pronombres_atonos(input_text) == expected_output


@pytest.mark.parametrize("input_text, expected_output", [
    # 4. Pronombre 'la' - Vocal 'a'
    ("la ayudaron", "l'ayudaron"),
    ("la agobiaron", "l'agobiaron"),
    ("la admira", "l'admira"),
    ("la abraza", "l'abraza"),
    # Mayúsculas
    ("La ayudaron", "L'ayudaron"),
    ("LA AGOBIARON", "L'AGOBIARON"),
    # 'la' con otras vocales o consonantes (no se modifica)
    ("la espera", "la espera"),
    ("la imagina", "la imagina"),
    ("la olvida", "la olvida"),
    ("la une", "la une"),
    ("la busca", "la busca"),
    ("La mira", "La mira"),
])
def test_pronombre_la_vocal(input_text, expected_output):
    assert transformar_pronombres_atonos(input_text) == expected_output


@pytest.mark.parametrize("input_text, expected_output", [
    # 5. Omisión de auxiliar en pretérito perfecto (me, te, se, le, la, lo)
    ("me he ido", "m'ido"),
    ("se ha enterado", "s'enterado"),
    ("te has enterado", "t'enterado"),
    ("lo he entendido", "l'entendido"),
    ("la ha agarrado", "l'agarrado"),
    ("le ha importado", "l'importado"),
    ("lo han olvidado", "l'olvidado"),
    ("se ha abierto", "s'abierto"),
    ("me he olvidado", "m'olvidado"),
    ("se ha escapado", "s'escapado"),
    ("me e ido", "m'ido"),
    ("se a enterado", "s'enterado"),
    # Mayúsculas
    ("Me he ido", "M'ido"),
    ("Se ha enterado", "S'enterado"),
    ("Lo he entendido", "L'entendido"),
    ("La ha agarrado", "L'agarrado"),
    ("LO HE ENTENDIDO", "L'ENTENDIDO"),
    ("LA HA AGARRADO", "L'AGARRADO"),
])
def test_pronombres_omision_auxiliar(input_text, expected_output):
    assert transformar_pronombres_atonos(input_text) == expected_output


@pytest.mark.parametrize("input_text, expected_output", [
    # 6. Falsos positivos en subcadenas
    ("la mesa redonda", "la mesa redonda"),
    ("el tema del día", "el tema del día"),
    ("la tela azul", "la tela azul"),
    ("la seta venenosa", "la seta venenosa"),
    ("lechuga", "lechuga"),
    ("loro", "loro"),
    ("lamento", "lamento"),
])
def test_evitar_falsos_positivos_pronombres(input_text, expected_output):
    assert transformar_pronombres_atonos(input_text) == expected_output


@pytest.mark.parametrize("input_text, expected_output", [
    # 7. Puntuación y casos borde
    ("¡Lo he entendido!", "¡L'entendido!"),
    ("¿No le importa?", "¿No l'importa?"),
    ("Hola, la ayudaron ayer", "Hola, l'ayudaron ayer"),
    (
        "Si lo ocultó y no le importa, la ayudaron",
        "Si l'ocultó y no l'importa, l'ayudaron"
    ),
    ("", ""),
])
def test_puntuacion_y_casos_borde_pronombres(input_text, expected_output):
    assert transformar_pronombres_atonos(input_text) == expected_output
