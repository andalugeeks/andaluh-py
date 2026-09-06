#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Tests unitarios para los artículos determinados 'el' y 'la'
"""

import pytest
from andaluh import (transformar_articulos,
                     transformar_articulo_el,
                     transformar_articulo_la, )


@pytest.mark.parametrize("input_text, expected_output", [
    # 1. Artículo 'el' - Regla l' (Entre vocales)
    ("echa el aceite", "echa l'aceite"),
    ("me pica el ojo", "me pica l'ojo"),
    ("compro el agua", "compro l'agua"),
    ("come el arroz", "come l'arroz"),
    ("pasa el invierno", "pasa l'invierno"),
    ("por el humo", "por el humo"),  # Precedido por consonante 'r'
    # Con tildes y circunflejos
    ("abre el árbol", "abre l'árbol"),
    ("mira el órgano", "mira l'órgano"),
    ("toca el ápice", "toca l'ápice"),
    # Mayúsculas
    ("Echa El Aceite", "Echa L'Aceite"),
    ("ECHA EL ACEITE", "ECHA L'ACEITE"),
])
def test_articulo_el_entre_vocales(input_text, expected_output):
    assert transformar_articulo_el(input_text) == expected_output


@pytest.mark.parametrize("input_text, expected_output", [
    # 2. Artículo 'el' - Regla 'r (Vocal a, e, o + Consonante posterior)
    ("conduce el coche", "conduce 'r coche"),
    ("mira el ratón", "mira 'r ratón"),
    ("mira el humo", "mira 'r humo"),
    ("toma el dinero", "toma 'r dinero"),
    ("pásame el pan", "pásame 'r pan"),
    ("compró el libro", "compró 'r libro"),
    ("canté el tango", "canté 'r tango"),
    ("dejó el vaso", "dejó 'r vaso"),
    # Mayúsculas
    ("Conduce El Coche", "Conduce 'r Coche"),
    ("CONDUCE EL COCHE", "CONDUCE 'R COCHE"),
])
def test_articulo_el_vocal_consonante(input_text, expected_output):
    assert transformar_articulo_el(input_text) == expected_output


@pytest.mark.parametrize("input_text, expected_output", [
    # 3. Artículo 'el' - Casos no modificados
    # Precedido por 'i' o 'u' y seguido de consonante
    ("comí el pan", "comí el pan"),
    ("escribí el texto", "escribí el texto"),
    ("un iglú el frío", "un iglú el frío"),
    # Precedido por consonante
    ("por el camino", "por el camino"),
    ("con el perro", "con el perro"),
    ("árbol el grande", "árbol el grande"),
    # Inicio de frase con consonante posterior
    ("El coche corre", "El coche corre"),
    ("El perro ladra", "El perro ladra"),
])
def test_articulo_el_no_modificado(input_text, expected_output):
    assert transformar_articulo_el(input_text) == expected_output


@pytest.mark.parametrize("input_text, expected_output", [
    # 4. Artículo 'la' - Regla l' (Vocal 'a' posterior)
    ("la almendra", "l'almendra"),
    ("la abeja", "l'abeja"),
    ("la abuela", "l'abuela"),
    ("la amiga", "l'amiga"),
    ("la acera", "l'acera"),
    ("la alegría", "l'alegría"),
    ("la agua", "l'agua"),
    ("la águila", "l'águila"),
    ("la âttitûh", "l'âttitûh"),
    # Mayúsculas
    ("La almendra", "L'almendra"),
    ("LA ALMENDRA", "L'ALMENDRA"),
    ("LA ABEJA", "L'ABEJA"),
])
def test_articulo_la_vocal_a_posterior(input_text, expected_output):
    assert transformar_articulo_la(input_text) == expected_output


@pytest.mark.parametrize("input_text, expected_output", [
    # 5. Artículo 'la' - Otras vocales y consonantes (no se modifica)
    ("la casa", "la casa"),
    ("la mesa", "la mesa"),
    ("la época", "la época"),
    ("la isla", "la isla"),
    ("la olla", "la olla"),
    ("la uva", "la uva"),
    ("La vaca", "La vaca"),
])
def test_articulo_la_no_modificado(input_text, expected_output):
    assert transformar_articulo_la(input_text) == expected_output


@pytest.mark.parametrize("input_text, expected_output", [
    # 6. Falsos positivos en subcadenas
    ("elenco", "elenco"),
    ("pelota", "pelota"),
    ("lago", "lago"),
    ("lana", "lana"),
    ("helado", "helado"),
    ("ella", "ella"),
])
def test_evitar_falsos_positivos_articulos(input_text, expected_output):
    assert transformar_articulos(input_text) == expected_output


@pytest.mark.parametrize("input_text, expected_output", [
    # 7. Combinación de el y la
    (
        "Echa el aceite en la almendra y conduce el coche",
        "Echa l'aceite en l'almendra y conduce 'r coche"
    ),
    (
        "Mira la abeja y toma el agua",
        "Mira l'abeja y toma l'agua"
    ),
    ("", ""),
])
def test_combinacion_articulos(input_text, expected_output):
    assert transformar_articulos(input_text) == expected_output
