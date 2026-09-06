#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4
"""
Módulo para la transformación y normalización fonético-ortográfica
de los pronombres átonos ('me', 'te', 'se', 'le', 'la', 'lo')
en castellano / andaluz.
"""

import re

# Conjunto exhaustivo de vocales (incluye tildes, diéresis y circunflejos)
ALL_VOWELS = set("aeiouáéíóúüâêîôûAEIOUÁÉÍÓÚÜÂÊÎÔÛ")

# Variantes de 'a' y 'o' (para pronombre 'lo')
AO_VOWELS = set("aoáóâôäöàòAOÁÓÂÔÄÖÀÒ")

# Variantes de 'a' (para pronombre 'la')
A_VOWELS = set("aáâäàAÁÂÄÀ")

# Caracteres alfabéticos válidos para palabras en español / andaluz
WORD_CHAR_PATTERN = r"[A-Za-zÁÉÍÓÚÜáéíóúüÂÊÎÔÛâêîôûÑñÇç]"

# Expresiones para vocales en patrones regex
ALL_VOWEL_CHARS = re.escape("".join(ALL_VOWELS))
AO_VOWEL_CHARS = re.escape("".join(AO_VOWELS))
A_VOWEL_CHARS = re.escape("".join(A_VOWELS))

# Formas del auxiliar haber (en español y transcripción EPA)
AUX_FORMS = (
    r"(?:he|ha|has|han|an|hâ|e|a|as|"
    r"HE|HA|HAS|HAN|AN|HÂ|E|A|AS|"
    r"He|Ha|Has|Han|An|Hâ)"
)

# Patrón para todos los pronombres átonos soportados
ALL_PRONOUNS_PATTERN = (
    r"(?:me|te|se|çe|ze|le|lo|la|"
    r"Me|Te|Se|Çe|Ze|Le|Lo|La|"
    r"ME|TE|SE|ÇE|ZE|LE|LO|LA)"
)


def is_vowel(char: str) -> bool:
    """Verifica si un carácter es una vocal."""
    return char in ALL_VOWELS


def is_ao_vowel(char: str) -> bool:
    """Verifica si un carácter es 'a' u 'o'."""
    return char in AO_VOWELS


def is_a_vowel(char: str) -> bool:
    """Verifica si un carácter es 'a'."""
    return char in A_VOWELS


def _get_apostrophe(pronoun: str) -> str:
    """Devuelve la forma apostrofada según el pronombre y mayúscula."""
    letter = pronoun[0]
    if pronoun.isupper() or letter.isupper():
        return f"{letter.upper()}'"
    return f"{letter.lower()}'"


def transformar_pronombres_atonos(texto: str) -> str:
    """
    Transforma los pronombres átonos ('me', 'te', 'se', 'le', 'la', 'lo'):

    1. Omisión de auxiliar en Pretérito Perfecto:
       - 'me', 'te', 'se', 'le', 'lo', 'la' + auxiliar + vocal
         Ejemplos:
           - "me he ido"        -> "m'ido"
           - "se ha enterado"   -> "s'enterado"
           - "te has enterado"  -> "t'enterado"
           - "lo he entendido"  -> "l'entendido"
           - "la ha agarrado"   -> "l'agarrado"
           - "le ha importado"  -> "l'importado"

    2. Reglas generales directas:
       - 'me', 'te', 'se' + cualquier vocal -> 'm\'', 't\'', 's\''
       - 'le' + cualquier vocal o 'han'/'an' -> 'l\''
         Ejemplos: "no le importa" -> "no l'importa"
       - 'lo' + vocal 'a' u 'o' -> 'l\''
         Ejemplos: "lo ocultó" -> "l'ocultó", "lo olvidaron" -> "l'olvidaron"
       - 'la' + vocal 'a' -> 'l\''
         Ejemplos: "la ayudaron" -> "l'ayudaron"

    Args:
        texto (str): Cadena de texto de entrada.

    Returns:
        str: Texto con los pronombres átonos transformados.
    """
    if not texto:
        return texto

    # 1. Omisión de auxiliar: [pronombre] + [auxiliar] + [vocal...]
    aux_pattern = re.compile(
        rf"\b({ALL_PRONOUNS_PATTERN})\s+"
        rf"{AUX_FORMS}\s+"
        rf"([{ALL_VOWEL_CHARS}]{WORD_CHAR_PATTERN}*)",
        re.UNICODE
    )

    def aux_replace(match):
        pronoun = match.group(1)
        next_word = match.group(2)
        apostrophe = _get_apostrophe(pronoun)
        return f"{apostrophe}{next_word}"

    texto = aux_pattern.sub(aux_replace, texto)

    # 2. Casos directos para 'le': seguido de 'han' / 'an' / 'ha' + consonante
    le_aux_direct_pattern = re.compile(
        r"\b(le|Le|LE)\s+(han|an|ha|Han|An|Ha|HAN|AN|HA)\b",
        re.UNICODE
    )

    def le_aux_replace(match):
        pronoun = match.group(1)
        aux = match.group(2)
        is_up = pronoun.isupper() or pronoun[0].isupper()
        apostrophe = "L'" if is_up else "l'"
        return f"{apostrophe}{aux}"

    texto = le_aux_direct_pattern.sub(le_aux_replace, texto)

    # 3. Regla directa: me, te, se, çe, ze, le + cualquier vocal
    all_vowel_pronouns = re.compile(
        rf"\b(me|te|se|çe|ze|le|Me|Te|Se|Çe|Ze|Le|ME|TE|SE|ÇE|ZE|LE)\s+"
        rf"([{ALL_VOWEL_CHARS}]{WORD_CHAR_PATTERN}*)",
        re.UNICODE
    )

    def all_vowel_replace(match):
        pronoun = match.group(1)
        next_word = match.group(2)
        apostrophe = _get_apostrophe(pronoun)
        return f"{apostrophe}{next_word}"

    texto = all_vowel_pronouns.sub(all_vowel_replace, texto)

    # 4. Regla directa: lo + vocal 'a' u 'o'
    lo_pattern = re.compile(
        rf"\b(lo|Lo|LO)\s+"
        rf"([{AO_VOWEL_CHARS}]{WORD_CHAR_PATTERN}*)",
        re.UNICODE
    )

    def lo_replace(match):
        pronoun = match.group(1)
        next_word = match.group(2)
        is_up = pronoun.isupper() or pronoun[0].isupper()
        apostrophe = "L'" if is_up else "l'"
        return f"{apostrophe}{next_word}"

    texto = lo_pattern.sub(lo_replace, texto)

    # 5. Regla directa: la + vocal 'a'
    la_pattern = re.compile(
        rf"\b(la|La|LA)\s+"
        rf"([{A_VOWEL_CHARS}]{WORD_CHAR_PATTERN}*)",
        re.UNICODE
    )

    def la_replace(match):
        pronoun = match.group(1)
        next_word = match.group(2)
        is_up = pronoun.isupper() or pronoun[0].isupper()
        apostrophe = "L'" if is_up else "l'"
        return f"{apostrophe}{next_word}"

    texto = la_pattern.sub(la_replace, texto)

    return texto
