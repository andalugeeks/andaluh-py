#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Tests unitarios para la función transformar_preposicion_de
"""

import pytest
from andaluh import transformar_preposicion_de


@pytest.mark.parametrize("input_text, expected_output", [
    # Regla 1: de + vocal -> d'vocal (minúsculas)
    ("de algo", "d'algo"),
    ("de ellos", "d'ellos"),
    ("de un amigo", "d'un amigo"),
    ("de interés", "d'interés"),
    ("de oro", "d'oro"),
    ("de árbol", "d'árbol"),
    ("de época", "d'época"),
    ("de índole", "d'índole"),
    ("de órganos", "d'órganos"),
    ("de útiles", "d'útiles"),
    # Regla 1: de + vocal (Mayúsculas / TitleCase)
    ("De acuerdo", "D'acuerdo"),
    ("De ellos", "D'ellos"),
    ("DE ALGO", "D'ALGO"),
    ("VASO DE AGUA", "VASO D'AGUA"),
])
def test_regla_1_vocal_posterior(input_text, expected_output):
    assert transformar_preposicion_de(input_text) == expected_output


@pytest.mark.parametrize("input_text, expected_output", [
    # Regla 2: vocal + de + consonante -> vocal 'e consonante
    ("puñado de cerezas", "puñado 'e cerezas"),
    ("sopa de fideos", "sopa 'e fideos"),
    ("casa de madera", "casa 'e madera"),
    ("café de Colombia", "café 'e Colombia"),
    ("menú de mediodía", "menú 'e mediodía"),
    ("mamá de Pedro", "mamá 'e Pedro"),
    ("colibrí de colores", "colibrí 'e colores"),
    ("dominó de madera", "dominó 'e madera"),
    # Regla 2: Mayúsculas
    ("PUÑADO DE CEREZAS", "PUÑADO 'E CEREZAS"),
    ("Puñado De Cerezas", "Puñado 'e Cerezas"),
])
def test_regla_2_vocal_anterior_consonante(input_text, expected_output):
    assert transformar_preposicion_de(input_text) == expected_output


@pytest.mark.parametrize("input_text, expected_output", [
    # Regla 3: vocal + de + vocal -> vocal d'vocal (prevalece regla d')
    ("carta de un", "carta d'un"),
    ("vaso de agua", "vaso d'agua"),
    ("copa de anís", "copa d'anís"),
    ("pedazo de idiota", "pedazo d'idiota"),
    ("trozo de embutido", "trozo d'embutido"),
    ("CARTA DE UN", "CARTA D'UN"),
])
def test_regla_3_prioridad_vocal_posterior(input_text, expected_output):
    assert transformar_preposicion_de(input_text) == expected_output


@pytest.mark.parametrize("input_text, expected_output", [
    # Consonante + de + consonante (no cambia)
    ("árbol de navidad", "árbol de navidad"),
    ("papel de regalo", "papel de regalo"),
    ("reloj de pared", "reloj de pared"),
    ("mes de mayo", "mes de mayo"),
    ("cantar de gesta", "cantar de gesta"),
    # Inicio de frase con consonante posterior (no cambia)
    (
        "De noche todos los gatos son pardos",
        "De noche todos los gatos son pardos"
    ),
    ("De Madrid al cielo", "De Madrid al cielo"),
    ("De pronto ocurrió", "De pronto ocurrió"),
])
def test_casos_no_modificados(input_text, expected_output):
    assert transformar_preposicion_de(input_text) == expected_output


@pytest.mark.parametrize("input_text, expected_output", [
    ("dedo de madera", "dedo 'e madera"),
    ("desde donde sea", "desde donde sea"),
    ("conde de Montecristo", "conde 'e Montecristo"),
    ("modelo de desarrollo", "modelo 'e desarrollo"),
    ("grande de España", "grande d'España"),
    ("grande de tamaño", "grande 'e tamaño"),
])
def test_evitar_falsos_positivos_subcadenas(input_text, expected_output):
    assert transformar_preposicion_de(input_text) == expected_output


@pytest.mark.parametrize("input_text, expected_output", [
    # Pausa sintáctica antes de 'de'
    ("Hola, de verdad", "Hola, de verdad"),
    ("¿De verdad?", "¿De verdad?"),
    ("¡De acuerdo!", "¡D'acuerdo!"),
    ("El coche (de carreras)", "El coche (de carreras)"),
    ("El coche (de época)", "El coche (d'época)"),
    # Múltiples 'de' en una misma frase
    (
        "Un trozo de tarta de manzana de otro día",
        "Un trozo 'e tarta 'e manzana d'otro día"
    ),
    (
        "El hijo de Antonio de la Torre",
        "El hijo d'Antonio 'e la Torre"
    ),
    # Cadenas vacías y límites
    ("", ""),
    ("El final de", "El final de"),
    ("Vengo de", "Vengo de"),
])
def test_puntuacion_y_casos_borde(input_text, expected_output):
    assert transformar_preposicion_de(input_text) == expected_output
