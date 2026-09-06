#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4
"""
Módulo para la transformación y normalización fonético-ortográfica
del adverbio 'ya' en castellano / andaluz.
"""

import re

# Conjunto de variantes de la vocal 'a' (incluye tildes y circunflejos)
A_VOWELS = set("aáâäàAÁÂÄÀ")

# Caracteres alfabéticos válidos para palabras en español / andaluz
WORD_CHAR_PATTERN = r"[A-Za-zÁÉÍÓÚÜáéíóúüÂÊÎÔÛâêîôûÑñÇç]"


def is_a_vowel(char: str) -> bool:
    """Verifica si un carácter es una variante de la vocal 'a'."""
    return char in A_VOWELS


def transformar_adverbio_ya(texto: str) -> str:
    """
    Transforma el adverbio 'ya' según la siguiente regla fonética:

    Regla y' (Vocal 'a' posterior):
       Si la palabra que sigue al adverbio 'ya' comienza por la letra
       'a' (o 'á', 'â'), el adverbio se transforma en 'y\\'' (o 'Y\\'')
       y se elide el espacio intermedio que lo une a dicha palabra.
       Ejemplos:
         - "ya acaba"   -> "y'acaba"
         - "ya almorzó" -> "y'almorzó"
         - "Ya abrió"   -> "Y'abrió"
         - "YA ACABÓ"   -> "Y'ACABÓ"

    Si la palabra siguiente empieza por cualquier otra vocal (e, i, o, u)
    o consonante, el adverbio se mantiene intacto ("ya", "Ya", "YA").
       Ejemplos:
         - "ya está"    -> "ya está"
         - "ya viene"   -> "ya viene"

    Args:
        texto (str): Cadena de texto de entrada.

    Returns:
        str: Texto resultante con el adverbio 'ya' transformado.
    """
    if not texto:
        return texto

    # Identificar el adverbio 'ya' como token aislado
    ya_pattern = re.compile(r"\b(ya|Ya|YA|yA)\b")

    # Busca los espacios y la palabra inmediatamente posterior
    next_word_pattern = re.compile(rf"^(\s+)({WORD_CHAR_PATTERN}+)")

    result = []
    last_idx = 0

    for match in ya_pattern.finditer(texto):
        start, end = match.span()
        ya_token = match.group(1)

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
        is_upper = ya_token.isupper()
        is_title = ya_token[0].isupper() and not is_upper

        if next_starts_a:
            apostrophe_ya = "Y'" if (is_upper or is_title) else "y'"
            result.append(apostrophe_ya)
            # Elidir el espacio posterior uniendo y' a la siguiente palabra
            last_idx = end + len(whitespace_after)
        else:
            result.append(ya_token)
            last_idx = end

    # Añadir el resto de la cadena
    result.append(texto[last_idx:])
    return "".join(result)
