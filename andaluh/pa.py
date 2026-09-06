#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4
"""
Módulo para la transformación y normalización fonético-ortográfica
de la preposición 'pa' en castellano / andaluz.
"""

import re

# Conjunto de variantes de la vocal 'a' (incluye tildes y circunflejos)
A_VOWELS = set("aáâäàAÁÂÄÀ")

# Caracteres alfabéticos válidos para palabras en español / andaluz
WORD_CHAR_PATTERN = r"[A-Za-zÁÉÍÓÚÜáéíóúüÂÊÎÔÛâêîôûÑñÇç]"


def is_a_vowel(char: str) -> bool:
    """Verifica si un carácter es una variante de la vocal 'a'."""
    return char in A_VOWELS


def transformar_preposicion_pa(texto: str) -> str:
    """
    Transforma la preposición 'pa' según la siguiente regla fonética:

    Regla p' (Vocal 'a' posterior):
       Si la palabra siguiente empieza por la letra 'a' (o 'á', 'â'),
       la preposición se convierte en 'p\\'' (o 'P\\'') y se elide el espacio
       que la une a la palabra.
       Ejemplo: 'pa abajo' -> 'p\\'abajo', 'pa almorzâ' -> 'p\\'almorzâ'.

    Si la siguiente palabra empieza por otra vocal o consonante, se mantiene.
       Ejemplo: 'pa ellos' -> 'pa ellos', 'pa ti' -> 'pa ti'.

    Args:
        texto (str): Cadena de texto de entrada.

    Returns:
        str: Texto con la preposición 'pa' transformada.
    """
    if not texto:
        return texto

    # Identificar la preposición 'pa' como token aislado
    pa_pattern = re.compile(r"\b(pa|Pa|PA|pA)\b")

    # Busca los espacios y la palabra inmediatamente posterior
    next_word_pattern = re.compile(rf"^(\s+)({WORD_CHAR_PATTERN}+)")

    result = []
    last_idx = 0

    for match in pa_pattern.finditer(texto):
        start, end = match.span()
        pa_token = match.group(1)

        # Añadir el texto previo no modificado
        result.append(texto[last_idx:start])

        # Analizar contexto léxico posterior
        text_after = texto[end:]
        next_match = next_word_pattern.search(text_after)

        if next_match:
            whitespace_after = next_match.group(1)
            next_word = next_match.group(2)
        else:
            whitespace_after = ""
            next_word = None

        next_starts_a = is_a_vowel(next_word[0]) if next_word else False

        # Preservar mayúsculas y minúsculas
        is_upper = pa_token.isupper()
        is_title = pa_token[0].isupper() and not is_upper

        # Regla p': Si la siguiente palabra empieza por 'a' / 'á' / 'â'
        if next_starts_a:
            apostrophe_pa = "P'" if (is_upper or is_title) else "p'"
            result.append(apostrophe_pa)
            # Elidir el espacio posterior uniendo 'p\'' a la siguiente palabra
            last_idx = end + len(whitespace_after)
        else:
            result.append(pa_token)
            last_idx = end

    # Añadir el resto de la cadena
    result.append(texto[last_idx:])
    return "".join(result)
