#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Tests unitarios para el módulo de contracciones unificadas y flag en epa()
"""

import pytest
import andaluh


@pytest.mark.parametrize("input_text, expected_output", [
    # Combinación de pronombres, artículos, en, de, pa, ya
    (
        "Vaso de agua para el niño y tira pa abajo porque ya acaba",
        "Vaso d'agua para 'r niño y tira p'abajo porque y'acaba"
    ),
    (
        "Un trozo de queso y vamos pa almorzar que ya abrió",
        "Un trozo 'e queso y vamos p'almorzar que y'abrió"
    ),
    (
        "Puñado de cerezas pa Antonio que ya almorzó",
        "Puñado 'e cerezas p'Antonio que y'almorzó"
    ),
    (
        "Ya acaba de hablar y tira pa allá",
        "Y'acaba 'e hablar y tira p'allá"
    ),
    (
        "Me he ido de viaje pa almorzar que ya acaba",
        "M'ido 'e viaje p'almorzar que y'acaba"
    ),
    (
        "Se ha enterado de todo y se entra pa adentro",
        "S'enterado 'e todo y s'entra p'adentro"
    ),
    (
        "Te has olvidado de la carta p'ayer que ya acabó",
        "T'olvidado 'e la carta p'ayer que y'acabó"
    ),
    (
        "Echa el aceite en la ensalada de la abuela",
        "Echa l'aceite 'n la ensalada 'e l'abuela"
    ),
    (
        "Conduce el coche pa ver la almendra",
        "Conduce 'r coche pa ver l'almendra"
    ),
    (
        "No le importa que lo he entendido y la ha agarrado",
        "No l'importa que l'entendido y l'agarrado"
    ),
    (
        "Lo ocultó pa ayer y le han dado el dinero",
        "L'ocultó p'ayer y l'han dado 'r dinero"
    ),
    (
        "Está en el avión y se sentará en la silla",
        "Está n'el avión y se sentará 'n la silla"
    ),
    (
        "Ocurrió en el altillo de la casa",
        "Ocurrió n'el altillo 'e la casa"
    ),
])
def test_apply_contractions_direct(input_text, expected_output):
    assert andaluh.apply_contractions(input_text) == expected_output
    assert andaluh.aplicar_contracciones(input_text) == expected_output


def test_epa_with_contractions_flag():
    # Sin contracciones (por defecto):
    text = "Me he ido con un vaso de agua y tira pa abajo que ya acaba"
    trans_default = andaluh.epa(text)
    trans_no_contr = andaluh.epa(text, contractions=False)
    assert trans_default == trans_no_contr
    # 'de', 'pa' y 'ya' se mantienen sin apostrofar
    assert "de agua" in trans_default
    assert "pa abaho" in trans_default
    assert "ya acaba" in trans_default

    # Con contracciones (contractions=True):
    trans_with_contr = andaluh.epa(text, contractions=True)
    assert "M'ido" in trans_with_contr
    assert "d'agua" in trans_with_contr
    assert "p'abaho" in trans_with_contr
    assert "y'acaba" in trans_with_contr


def test_apply_contractions_empty():
    assert andaluh.apply_contractions("") == ""
    assert andaluh.aplicar_contracciones("") == ""
