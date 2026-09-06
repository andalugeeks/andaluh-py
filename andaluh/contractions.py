#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4
"""
Módulo unificado para la gestión de contracciones fonético-ortográficas.
"""

from andaluh.de import transformar_preposicion_de
from andaluh.en import transformar_preposicion_en
from andaluh.pa import transformar_preposicion_pa
from andaluh.ya import transformar_adverbio_ya
from andaluh.pronombres import transformar_pronombres_atonos
from andaluh.articulos import transformar_articulos


def apply_contractions(texto: str) -> str:
    """
    Aplica todas las contracciones fonéticas y ortográficas soportadas:
    - Pronombres átonos 'me', 'te', 'se', 'le', 'la', 'lo' (m', t', s', l')
    - Preposición 'en' (n'el, 'n) - Ejecutada antes para prioridad n'el
    - Artículos determinados 'el', 'la' (l', 'r)
    - Preposición 'de' (d', 'e)
    - Preposición 'pa' (p')
    - Adverbio 'ya' (y')

    Args:
        texto (str): Cadena de texto de entrada.

    Returns:
        str: Texto con todas las contracciones aplicadas.
    """
    if not texto:
        return texto

    texto = transformar_pronombres_atonos(texto)
    texto = transformar_preposicion_en(texto)
    texto = transformar_articulos(texto)
    texto = transformar_preposicion_de(texto)
    texto = transformar_preposicion_pa(texto)
    texto = transformar_adverbio_ya(texto)
    return texto


# Alias en español para la API
aplicar_contracciones = apply_contractions
