#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4
"""
Módulo para la transformación y normalización fonético-ortográfica
de la preposición 'en' en castellano / andaluz.
"""

import re

# Vocales completas
ALL_VOWELS = set("aeiouáéíóúüâêîôûäëïöàèìòùAEIOUÁÉÍÓÚÜÂÊÎÔÛÄËÏÖÀÈÌÒÙ")

# Vocales 'a', 'e', 'o' (con variantes de tildes y circunflejos)
AEO_VOWELS = set("aeoáéóâêôäëöàèòAEOÁÉÓÂÊÔÄËÖÀÈÒ")

# Caracteres alfabéticos válidos para palabras en español / andaluz
WORD_CHAR_PATTERN = r"[A-Za-zÁÉÍÓÚÜáéíóúüÂÊÎÔÛâêîôûÑñÇç]"


def is_vowel(char: str) -> bool:
    """Verifica si un carácter es una vocal."""
    return char in ALL_VOWELS


def is_aeo_vowel(char: str) -> bool:
    """Verifica si un carácter es una vocal 'a', 'e' u 'o'."""
    return char in AEO_VOWELS


def is_consonant(char: str) -> bool:
    """Verifica si un carácter es una consonante alfabética."""
    return char.isalpha() and not is_vowel(char)


def transformar_preposicion_en(texto: str) -> str:
    """
    Transforma la preposición 'en' según las siguientes reglas fonéticas:

    1. Regla de Combinación de Prioridad con el Artículo 'el' (n'el / n'er):
       Cuando 'en' va seguida de 'el' (o 'er'), prevalece la contracción
       unificada 'n\\'el' (o 'N\\'el', 'N\\'EL') y bloquea cualquier
       apostrofación posterior sobre el artículo.
       Ejemplos:
         - "está en el avión"   -> "está n'el avión"
         - "ocurrió en el árbol" -> "ocurrió n'el árbol"
         - "En el coche"        -> "N'el coche"
         - "EN EL AVIÓN"        -> "N'EL AVIÓN"

    2. Regla 'n (Vocal a, e, o + Consonante posterior):
       Si la palabra anterior termina en 'a', 'e', 'o' Y la siguiente
       comienza por consonante, 'en' se apostrofa como ''n' (o ''N').
       Ejemplos:
         - "iré en cinco"         -> "iré 'n cinco"
         - "estará en Granada"    -> "estará 'n Granada"
         - "sentarse en la silla" -> "sentarse 'n la silla"

    Args:
        texto (str): Cadena de texto de entrada.

    Returns:
        str: Texto con la preposición 'en' transformada.
    """
    if not texto:
        return texto

    # 1. Regla Prioridad: en + el / en + er -> n'el / n'er
    en_el_pattern = re.compile(
        r"\b(en|En|EN|eN)\s+(el|El|EL|eL|er|Er|ER)\b",
        re.UNICODE
    )

    def en_el_replace(match):
        en_tok = match.group(1)
        el_tok = match.group(2)
        is_er = el_tok.lower() == "er"
        article_part = "er" if is_er else "el"

        if en_tok.isupper() and el_tok.isupper():
            return f"N'{article_part.upper()}"
        elif en_tok[0].isupper():
            return f"N'{article_part}"
        return f"n'{article_part}"

    texto = en_el_pattern.sub(en_el_replace, texto)

    # 2. Regla 'n: Vocal a, e, o anterior + Consonante posterior
    en_pattern = re.compile(r"\b(en|En|EN|eN)\b")
    prev_word_pattern = re.compile(rf"({WORD_CHAR_PATTERN}+)\s+$")
    next_word_pattern = re.compile(rf"^\s+({WORD_CHAR_PATTERN}+)")

    result = []
    last_idx = 0

    for match in en_pattern.finditer(texto):
        start, end = match.span()
        en_token = match.group(1)

        result.append(texto[last_idx:start])

        # Analizar palabra anterior
        text_before = texto[:start]
        prev_match = prev_word_pattern.search(text_before)
        prev_word = prev_match.group(1) if prev_match else None

        # Analizar palabra posterior
        text_after = texto[end:]
        next_match = next_word_pattern.search(text_after)
        next_word = next_match.group(1) if next_match else None

        prev_ends_aeo = is_aeo_vowel(prev_word[-1]) if prev_word else False
        next_starts_consonant = (
            is_consonant(next_word[0]) if next_word else False
        )

        is_upper = en_token.isupper()

        if prev_ends_aeo and next_starts_consonant:
            n_token = "'N" if is_upper else "'n"
            result.append(n_token)
            last_idx = end
        else:
            result.append(en_token)
            last_idx = end

    result.append(texto[last_idx:])
    return "".join(result)
