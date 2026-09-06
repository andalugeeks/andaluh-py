#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4
"""
Módulo para la transformación y normalización fonético-ortográfica
de los artículos determinados 'el' y 'la' en castellano / andaluz.
"""

import re

# Vocales completas
ALL_VOWELS = set("aeiouáéíóúüâêîôûäëïöàèìòùAEIOUÁÉÍÓÚÜÂÊÎÔÛÄËÏÖÀÈÌÒÙ")

# Vocales 'a', 'e', 'o' (con variantes de tildes y circunflejos)
AEO_VOWELS = set("aeoáéóâêôäëöàèòAEOÁÉÓÂÊÔÄËÖÀÈÒ")

# Variantes de la vocal 'a'
A_VOWELS = set("aáâäàAÁÂÄÀ")

# Caracteres alfabéticos válidos para palabras en español / andaluz
WORD_CHAR_PATTERN = r"[A-Za-zÁÉÍÓÚÜáéíóúüÂÊÎÔÛâêîôûÑñÇç]"


def is_vowel(char: str) -> bool:
    """Verifica si un carácter es una vocal."""
    return char in ALL_VOWELS


def is_aeo_vowel(char: str) -> bool:
    """Verifica si un carácter es una vocal 'a', 'e' u 'o'."""
    return char in AEO_VOWELS


def is_a_vowel(char: str) -> bool:
    """Verifica si un carácter es una variante de la vocal 'a'."""
    return char in A_VOWELS


def is_consonant(char: str) -> bool:
    """Verifica si un carácter es una consonante alfabética."""
    return char.isalpha() and not is_vowel(char)


def transformar_articulo_el(texto: str) -> str:
    """
    Transforma el artículo 'el' según las siguientes reglas fonéticas:

    1. Regla l' (Entre vocales):
       Si la palabra anterior termina en vocal Y la siguiente comienza
       por vocal, 'el' se apostrofa como 'l\\'' (o 'L\\'') y se elide el
       espacio que lo une a la palabra siguiente.
       Ejemplo: 'echa el aceite' -> 'echa l\\'aceite'.

    2. Regla 'r (Vocal a, e, o + Consonante posterior):
       Si la palabra anterior termina en 'a', 'e', 'o' Y la siguiente
       comienza por consonante, 'el' se transforma en ''r' (o ''R').
       Ejemplo: 'conduce el coche' -> 'conduce \\'r coche'.
    """
    if not texto:
        return texto

    el_pattern = re.compile(r"\b(el|El|EL|eL|er|Er|ER)\b")
    prev_word_pattern = re.compile(rf"({WORD_CHAR_PATTERN}+)\s+$")
    next_word_pattern = re.compile(rf"^(\s+)({WORD_CHAR_PATTERN}+)")

    result = []
    last_idx = 0

    for match in el_pattern.finditer(texto):
        start, end = match.span()
        el_token = match.group(1)

        result.append(texto[last_idx:start])

        # Analizar palabra anterior
        text_before = texto[:start]
        prev_match = prev_word_pattern.search(text_before)
        prev_word = prev_match.group(1) if prev_match else None

        # Analizar palabra posterior
        text_after = texto[end:]
        next_match = next_word_pattern.search(text_after)

        if next_match:
            whitespace_after = next_match.group(1)
            next_word = next_match.group(2)
        else:
            whitespace_after = ""
            next_word = None

        prev_ends_vowel = is_vowel(prev_word[-1]) if prev_word else False
        prev_ends_aeo = is_aeo_vowel(prev_word[-1]) if prev_word else False
        next_starts_vowel = is_vowel(next_word[0]) if next_word else False
        next_starts_consonant = (
            is_consonant(next_word[0]) if next_word else False
        )

        is_upper = el_token.isupper()
        is_title = el_token[0].isupper() and not is_upper

        # 1. Regla l' (Entre vocales)
        if prev_ends_vowel and next_starts_vowel:
            apostrophe_el = "L'" if (is_upper or is_title) else "l'"
            result.append(apostrophe_el)
            last_idx = end + len(whitespace_after)
        # 2. Regla 'r (Vocal a, e, o + Consonante posterior)
        elif prev_ends_aeo and next_starts_consonant:
            r_token = "'R" if is_upper else "'r"
            result.append(r_token)
            last_idx = end
        else:
            result.append(el_token)
            last_idx = end

    result.append(texto[last_idx:])
    return "".join(result)


def transformar_articulo_la(texto: str) -> str:
    """
    Transforma el artículo 'la' según la siguiente regla fonética:

    Regla l' (Vocal 'a' posterior):
       Si la palabra siguiente comienza por 'a', 'á', 'â', el artículo 'la'
       se apostrofa como 'l\\'' (o 'L\\'') y se elide el espacio intermedio.
       Ejemplo: 'la almendra' -> 'l\\'almendra', 'la abeja' -> 'l\\'abeja'.
    """
    if not texto:
        return texto

    la_pattern = re.compile(r"\b(la|La|LA|lA)\b")
    next_word_pattern = re.compile(rf"^(\s+)({WORD_CHAR_PATTERN}+)")

    result = []
    last_idx = 0

    for match in la_pattern.finditer(texto):
        start, end = match.span()
        la_token = match.group(1)

        result.append(texto[last_idx:start])

        text_after = texto[end:]
        next_match = next_word_pattern.search(text_after)

        if next_match:
            whitespace_after = next_match.group(1)
            next_word = next_match.group(2)
        else:
            whitespace_after = ""
            next_word = None

        next_starts_a = is_a_vowel(next_word[0]) if next_word else False

        is_upper = la_token.isupper()
        is_title = la_token[0].isupper() and not is_upper

        if next_starts_a:
            apostrophe_la = "L'" if (is_upper or is_title) else "l'"
            result.append(apostrophe_la)
            last_idx = end + len(whitespace_after)
        else:
            result.append(la_token)
            last_idx = end

    result.append(texto[last_idx:])
    return "".join(result)


def transformar_articulos(texto: str) -> str:
    """Aplica las transformaciones para los artículos 'el' y 'la'."""
    if not texto:
        return texto
    texto = transformar_articulo_el(texto)
    texto = transformar_articulo_la(texto)
    return texto
