#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4
"""
Módulo para la transformación y normalización fonético-ortográfica
de la preposición 'de' en castellano / andaluz.
"""

import re

# Conjunto exhaustivo de vocales (incluye tildes, diéresis y circunflejos)
VOWELS = set("aeiouáéíóúüâêîôûAEIOUÁÉÍÓÚÜÂÊÎÔÛ")

# Caracteres alfabéticos válidos para palabras en español / andaluz
WORD_CHAR_PATTERN = r"[A-Za-zÁÉÍÓÚÜáéíóúüÂÊÎÔÛâêîôûÑñÇç]"


def is_vowel(char: str) -> bool:
    """Verifica si un carácter es una vocal (incluyendo tildes)."""
    return char in VOWELS


def is_consonant(char: str) -> bool:
    """Verifica si un carácter es una consonante alfabética."""
    return char.isalpha() and not is_vowel(char)


def transformar_preposicion_de(texto: str) -> str:
    """
    Transforma la preposición 'de' según las siguientes reglas fonéticas:

    1. Regla d' (Vocal posterior):
       Si la palabra siguiente empieza por vocal, la preposición se convierte
       en 'd\\'' (o 'D\\'') y se elide el espacio que la une a la palabra.
       Ejemplo: 'de algo' -> 'd\\'algo'.

    2. Regla 'e (Vocal anterior + Consonante posterior):
       Si la palabra anterior termina en vocal Y la palabra posterior empieza
       por consonante, la preposición se convierte en ''e' (o ''E').
       Ejemplo: 'puñado de cerezas' -> 'puñado \\'e cerezas'.

    3. Regla de Prioridad (Vocal anterior + Vocal posterior):
       Si la palabra anterior termina en vocal Y la posterior
       empieza por vocal, prevalece la regla d'.
       Ejemplo: 'carta de un' -> 'carta d\\'un'.

    4. Otros casos:
       Si la palabra anterior termina en consonante y la posterior empieza por
       consonante, o si está al inicio de frase seguida de consonante,
       se mantiene 'de'.

    Args:
        texto (str): Cadena de texto de entrada.

    Returns:
        str: Texto con las preposiciones 'de' transformadas.
    """
    if not texto:
        return texto

    # Identificar la preposición 'de' como token aislado
    de_pattern = re.compile(r"\b(de|De|DE|dE)\b")

    # Busca la palabra inmediatamente anterior (separada solo por espacios)
    prev_word_pattern = re.compile(rf"({WORD_CHAR_PATTERN}+)\s+$")

    # Busca los espacios y la palabra inmediatamente posterior
    next_word_pattern = re.compile(rf"^(\s+)({WORD_CHAR_PATTERN}+)")

    result = []
    last_idx = 0

    for match in de_pattern.finditer(texto):
        start, end = match.span()
        de_token = match.group(1)

        # Añadir el texto no modificado antes de esta coincidencia
        result.append(texto[last_idx:start])

        # 1. Analizar contexto léxico anterior
        text_before = texto[:start]
        prev_match = prev_word_pattern.search(text_before)
        prev_word = prev_match.group(1) if prev_match else None

        # 2. Analizar contexto léxico posterior
        text_after = texto[end:]
        next_match = next_word_pattern.search(text_after)

        if next_match:
            whitespace_after = next_match.group(1)
            next_word = next_match.group(2)
        else:
            whitespace_after = ""
            next_word = None

        # Evaluación de condiciones fonéticas
        prev_ends_vowel = is_vowel(prev_word[-1]) if prev_word else False
        next_starts_vowel = is_vowel(next_word[0]) if next_word else False
        next_starts_consonant = (
            is_consonant(next_word[0]) if next_word else False
        )

        # Preservar mayúsculas y minúsculas
        is_upper = de_token.isupper()
        is_title = de_token[0].isupper() and not is_upper

        # Regla 1 & 3: Vocal posterior (Prioridad máxima)
        if next_starts_vowel:
            apostrophe_de = "D'" if (is_upper or is_title) else "d'"
            result.append(apostrophe_de)
            # Elidir el espacio posterior uniendo 'd\'' a la siguiente palabra
            last_idx = end + len(whitespace_after)

        # Regla 2: Vocal anterior + Consonante posterior
        elif prev_ends_vowel and next_starts_consonant:
            e_token = "'E" if is_upper else "'e"
            result.append(e_token)
            last_idx = end

        # Caso por defecto: No aplica transformación
        else:
            result.append(de_token)
            last_idx = end

    # Añadir el resto de la cadena
    result.append(texto[last_idx:])
    return "".join(result)
