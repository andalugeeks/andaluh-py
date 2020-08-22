#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4
###
#
# Copyright (c) 2018-2020 Andalugeeks
# Authors:
# - Ksar Feui <a.moreno.losana@gmail.com>
# - J. Félix Ontañón <felixonta@gmail.com>
# - Sergio Soto <scots4ever@gmail.com>

import re
import random

from andaluh.defs import (VOWELS_ALL_NOTILDE,
                          H_RULES_EXCEPT,
                          VAF,
                          VVF,
                          GJ_RULES_EXCEPT,
                          V_RULES_EXCEPT,
                          LL_RULES_EXCEPT,
                          VOWELS_ALL_TILDE,
                          DIGRAPHS,
                          WORDEND_CONST_RULES_EXCEPT,
                          WORDEND_S_RULES_EXCEPT,
                          WORDEND_D_RULES_EXCEPT,
                          WORDEND_D_INTERVOWEL_RULES_EXCEPT,
                          ENDING_RULES_EXCEPTION, )
from functools import reduce


# Regex compilation.
# Words to ignore in the translitaration in escapeLinks mode.
to_ignore_re = re.compile('|'.join([
    # URLs, i.e. andaluh.es, www.andaluh.es, https://www.andaluh.es
    r'(?:[h|H][t|T][t|T][p|P][s|S]?://)?(?:www\.)?(?:[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z|A-Z]{2,6})',
    r'(?:@\w+\b)',  # Mentions, i.e. @andaluh
    r'(?:#\w+\b)',  # Hashtags, i.e. #andaluh
    r'(?=\b[MCDXLVI]{1,8}\b)M{0,4}(?:CM|CD|D?C{0,3})(?:XC|XL|L?X{0,3})(?:IX|IV|V?I{0,3})' # roman numerals
]),  re.UNICODE)

# Auxiliary functions


def get_vowel_circumflex(vowel):

    # If no tilde, replace with circumflex
    if vowel and vowel in VOWELS_ALL_NOTILDE:
        i = VOWELS_ALL_NOTILDE.find(vowel) + 5
        return VOWELS_ALL_NOTILDE[i: i + 1][0]

    # If vowel with tilde, leave it as it is
    elif vowel and vowel in VOWELS_ALL_TILDE:
        return vowel

    # You shouldn't call this method with a non vowel
    else:
        raise AndaluhError('Not a vowel', vowel)


def get_vowel_tilde(vowel):

    # If no tilde, replace with circumflex
    if vowel and vowel in VOWELS_ALL_NOTILDE:
        i = VOWELS_ALL_NOTILDE.find(vowel)
        return VOWELS_ALL_TILDE[i]

    # If vowel with tilde, leave it as it is
    elif vowel and vowel in VOWELS_ALL_TILDE:
        return vowel

    # You shouldn't call this method with a non vowel
    else:
        raise AndaluhError('Not a vowel', vowel)

# TODO: This can be improved to perform replacement in a per character basis
# NOTE: It assumes replacement_word to be already lowercase


def keep_case(word, replacement_word):
    if word.islower():
        return replacement_word
    elif word.isupper():
        return replacement_word.upper()
    elif word.istitle():
        return replacement_word.title()
    else:
        return replacement_word

# EPA replacement functions


def h_rules(text):
    """Supress mute /h/"""

    def replace_with_case(match):
        word = match.group(0)

        if word.lower() in list(H_RULES_EXCEPT.keys()):
            return keep_case(word, H_RULES_EXCEPT[word.lower()])
        else:
            def replace_with_case(match):
                h_char = match.group(1)
                next_char = match.group(2)

                if next_char and h_char.isupper():
                    return next_char.upper()
                elif next_char and h_char.islower():
                    return next_char.lower()
                else:
                    return ''

            return re.sub(
                r'(?<!c)(h)(\w?)',
                replace_with_case,
                word,
                flags=re.IGNORECASE)

    # chihuahua => chiguagua
    text = re.sub(r'(?<!c)(h)(ua)',
                  lambda match: 'g' + match.group(2) if match.group(1).islower() else 'G' + match.group(2), text, flags=re.IGNORECASE | re.UNICODE)  # NOQA: E501
    # cacahuete => cacagûete
    text = re.sub(
        r'(?<!c)(h)(u)(e)',
        lambda match: 'g' +
        keep_case(
            match.group(2),
            'ü') +
        match.group(3) if match.group(1).islower() else 'G' +
        keep_case(
            match.group(2),
            'ü') +
        match.group(3),
        text,
        flags=re.IGNORECASE | re.UNICODE)

    # General /h/ replacements
    text = re.sub(
        r'\b(\w*?)(h)(\w*?)\b',
        replace_with_case,
        text,
        flags=re.IGNORECASE | re.UNICODE)
    return text


def x_rules(text, vaf=VAF):
    """Replacement rules for /ks/ with EPA VAF"""

    def replace_with_case(match):
        x_char = match.group(1)

        if x_char.islower():
            return vaf
        else:
            return vaf.upper()

    def replace_intervowel_with_case(match):
        prev_char = match.group(1)
        x_char = match.group(2)
        next_char = match.group(3)

        prev_char = get_vowel_circumflex(prev_char)

        if x_char.isupper():
            return prev_char + vaf.upper() * 2 + next_char
        else:
            return prev_char + vaf * 2 + next_char

    # If the text begins with /ks/
    # Xilófono roto => Çilófono roto
    if text[0] == "X":
        text = vaf.upper() + text[1:]
    if text[0] == "x":
        text = vaf + text[1:]

    # If the /ks/ sound is between vowels
    # Axila => Aççila | Éxito => Éççito | Sexy => Çeççy
    text = re.sub(
        r'(a|e|i|o|u|á|é|í|ó|ú)(x)(a|e|i|o|u|y|á|é|í|ó|ú)',
        replace_intervowel_with_case,
        text,
        flags=re.IGNORECASE | re.UNICODE)

    # Every word starting with /ks/
    text = re.sub(r'\b(x)', replace_with_case, text,
                  flags=re.IGNORECASE | re.UNICODE)

    return text


def ch_rules(text):
    """Replacement rules for /∫/ (voiceless postalveolar fricative)"""

    text = re.sub(r'(c)(h)', lambda match: 'x' if match.group(
        1).islower() else 'X', text, flags=re.IGNORECASE)
    return text


def gj_rules(text, vvf=VVF):
    """Replacing /x/ (voiceless postalveolar fricative) with /h/"""

    def replace_h_with_case(match):
        word = match.group(0)

        if word.lower() in list(GJ_RULES_EXCEPT.keys()):
            return keep_case(word, GJ_RULES_EXCEPT[word.lower()])
        else:
            # TODO: This is an AWFUL way of implementing replacement rules with
            # exceptions. To be fixed.
            word = re.sub(
                r'(g|j)(e|i|é|í)',
                lambda match: vvf +
                match.group(2) if match.group(1).islower() else vvf.upper() +
                match.group(2),
                word,
                flags=re.IGNORECASE | re.UNICODE)
            word = re.sub(
                r'(j)(a|o|u|á|ó|ú)',
                lambda match: vvf +
                match.group(2) if match.group(1).islower() else vvf.upper() +
                match.group(2),
                word,
                flags=re.IGNORECASE | re.UNICODE)
            return word

    def replace_g_with_case(match):
        s = match.group('s')
        a = match.group('a')
        b = match.group('b')
        ue = match.group('ue')
        const = match.group('const')

        return s + a + keep_case(b, 'g') + ue + const

    text = re.sub(
        r'\b(\w*?)(g|j)(e|i|é|í)(\w*?)\b',
        replace_h_with_case,
        text,
        flags=re.IGNORECASE | re.UNICODE)
    text = re.sub(
        r'\b(\w*?)(j)(a|o|u|á|ó|ú)(\w*?)\b',
        replace_h_with_case,
        text,
        flags=re.IGNORECASE | re.UNICODE)

    # GUE,GUI replacement
    text = re.sub(r'(gu|gU)(e|i|é|í|E|I|É|Í)', r'g\2', text)
    text = re.sub(r'(Gu|GU)(e|i|é|í|E|I|É|Í)', r'G\2', text)

    # GÜE,GÜI replacement
    text = re.sub(r'(g|G)(ü)(e|i|é|í|E|I|É|Í)', r'\1u\3', text)
    text = re.sub(r'(g|G)(Ü)(e|i|é|í|E|I|É|Í)', r'\1U\3', text)

    # buen / abuel / sabues => guen / aguel / sagues
    # TODO: I've the gut feeling the following two regex can be merged into
    # one.
    text = re.sub(r'(b)(uen)', lambda match: 'g' +
                  match.group(2) if match.group(1).islower() else 'G' +
                  match.group(2), text, flags=re.IGNORECASE | re.UNICODE)
    text = re.sub(
        r'(?P<s>s?)(?P<a>a?)(?<!m)(?P<b>b)(?P<ue>ue)(?P<const>l|s)',
        replace_g_with_case,
        text,
        flags=re.IGNORECASE | re.UNICODE)

    return text


def v_rules(text):
    """Replacing all /v/ (Voiced labiodental fricative) with /b/"""

    def replace_with_case(match):
        word = match.group(0)

        if word.lower() in list(V_RULES_EXCEPT.keys()):
            return keep_case(word, V_RULES_EXCEPT[word.lower()])
        else:
            # NV -> NB -> MB (i.e.: envidia -> embidia)
            word = re.sub(
                r'nv',
                lambda match: keep_case(
                    match.group(0),
                    'mb'),
                word,
                flags=re.IGNORECASE | re.UNICODE)
            word = re.sub(r'v', r'b', word)
            word = re.sub(r'V', r'B', word)
            return word

    text = re.sub(
        r'\b(\w*?)(v)(\w*?)\b',
        replace_with_case,
        text,
        flags=re.IGNORECASE | re.UNICODE)
    return text


def ll_rules(text):
    """Replace ll digraph.

    Replacing /ʎ/ (digraph ll) with Greek Y for /ʤ/ sound (voiced
    postalveolar affricate)"""

    def replace_with_case(match):
        word = match.group(0)

        if word.lower() in list(LL_RULES_EXCEPT.keys()):
            return keep_case(word, LL_RULES_EXCEPT[word.lower()])
        else:
            return re.sub(r'(l)(l)', lambda match: 'Y' if match.group(
                1).isupper() else 'y', word, flags=re.IGNORECASE)

    text = re.sub(
        r'\b(\w*?)(l)(l)(\w*?)\b',
        replace_with_case,
        text,
        flags=re.IGNORECASE)
    return text


def l_rules(text):
    """Rotating /l/ with /r/"""

    text = re.sub(
        r'(l)(b|c|ç|Ç|g|s|d|f|g|h|k|m|p|q|r|t|x|z)',
        lambda match: 'r' +
        match.group(2) if match.group(1).islower() else 'R' +
        match.group(2),
        text,
        flags=re.IGNORECASE)
    return text


def psico_pseudo_rules(text):
    """Drops /p/ for pseudo- or psico- prefixes"""

    def replace_psicpseud_with_case(match):
        ps_syllable = match.group(1)

        if ps_syllable[0] == 'p':
            return ps_syllable[1:]
        else:
            return ps_syllable[1].upper() + ps_syllable[2:]

    text = re.sub(
        r'(psic|pseud)',
        replace_psicpseud_with_case,
        text,
        flags=re.IGNORECASE)
    return text


def vaf_rules(text, vaf=VAF):
    """Replacing Voiceless alveolar fricative (vaf) /s/ /θ/ with EPA's ç/Ç"""

    def replace_with_case(match):
        l_char = match.group(1)
        next_char = match.group(2)

        if l_char.islower():
            return vaf + next_char
        else:
            return vaf.upper() + next_char

    text = re.sub(
        r'(z|s)(a|e|i|o|u|á|é|í|ó|ú|â|ê|î|ô|û)',
        replace_with_case,
        text,
        flags=re.IGNORECASE | re.UNICODE)
    text = re.sub(r'(c)(e|i|é|í|ê|î)', replace_with_case,
                  text, flags=re.IGNORECASE | re.UNICODE)

    return text


def digraph_rules(text):
    """Replacement of consecutive consonant with EPA VAF"""

    def replace_lstrst_with_case(match):
        vowel_char = match.group(1)
        lr_char = match.group(2)
        t_char = match.group(4)

        if lr_char == 'l':
            lr_char == 'r'
        elif lr_char == 'L':
            lr_char == 'R'
        else:
            pass

        return vowel_char + lr_char + t_char * 2

    def replace_bdnr_s_with_case(match):
        vowel_char = match.group(1)
        cons_char = match.group(2)
        s_char = match.group(3)
        digraph_char = match.group(4)

        if cons_char.lower() + s_char.lower() == 'rs':
            return vowel_char + cons_char + digraph_char * 2
        else:
            return get_vowel_circumflex(vowel_char) + digraph_char * 2

    def replace_transpost_with_case(match):
        init_char = match.group(1)
        vowel_char = match.group(2)
        cons_char = match.group(4)

        if cons_char.lower() == 'l':
            return init_char + \
                get_vowel_circumflex(vowel_char) + cons_char + '-' + cons_char
        else:
            return init_char + get_vowel_circumflex(vowel_char) + cons_char * 2

    def replace_l_with_case(match):
        vowel_char = match.group(1)
        digraph_char = match.group(3)

        return get_vowel_circumflex(vowel_char) + \
            digraph_char + '-' + digraph_char

    def replace_digraph_with_case(match):
        vowel_char = match.group(1)
        to_drop_char, digraph_char = match.group(2)

        return get_vowel_circumflex(vowel_char) + digraph_char * 2

    # intersticial / solsticio / superstición / cárstico => interttiçiâh /
    # çorttiçio / çuperttiçión / cárttico
    text = re.sub(
        r'(a|e|i|o|u|á|é|í|ó|ú)(l|r)(s)(t)',
        replace_lstrst_with_case,
        text,
        flags=re.IGNORECASE)
    # aerotransporte => aerotrâpporte | translado => trâl-lado | transcendente
    # => trâççendente | postoperatorio => pôttoperatorio | postpalatal =>
    # pôppalatal
    text = re.sub(
        r'(tr|p)(a|o)(ns|st)(b|c|ç|Ç|d|f|g|h|j|k|l|m|n|p|q|s|t|v|w|x|y|z)',
        replace_transpost_with_case,
        text,
        flags=re.IGNORECASE | re.UNICODE)
    # abstracto => âttrâtto | adscrito => âccrito | perspectiva => pêrppêttiba
    text = re.sub(
        r'(a|e|i|o|u|á|é|í|ó|ú)(b|d|n|r)(s)(b|c|ç|Ç|d|f|g|h|j|k|l|m|n|p|q|s|t|v|w|x|y|z)',  # NOQA: 501
        replace_bdnr_s_with_case,
        text,
        flags=re.IGNORECASE | re.UNICODE)
    # atlántico => âl-lántico | orla => ôl-la | adlátere => âl-látere | tesla
    # => têl-la ...
    text = re.sub(
        r'(a|e|i|o|u|á|é|í|ó|ú)(d|j|r|s|t|x|z)(l)',
        replace_l_with_case,
        text,
        flags=re.IGNORECASE | re.UNICODE)

    # General digraph rules.
    text = re.sub(
        r'(a|e|i|o|u|á|é|í|ó|ú)(' + '|'.join(DIGRAPHS) + ')',
        replace_digraph_with_case,
        text,
        flags=re.IGNORECASE | re.UNICODE)

    return text


def word_ending_rules(text):  # noqa: C901

    def replace_d_end_with_case(match):
        unstressed_rules = {
            'a': 'â', 'A': 'Â', 'á': 'â', 'Á': 'Â',
            'e': 'ê', 'E': 'Ê', 'é': 'ê', 'É': 'Ê',
            'i': 'î', 'I': 'Î', 'í': 'î', 'Í': 'Î',
            'o': 'ô', 'O': 'Ô', 'ó': 'ô', 'Ó': 'Ô',
            'u': 'û', 'U': 'Û', 'ú': 'û', 'Ú': 'Û'
        }

        stressed_rules = {
            'a': 'á', 'A': 'Á', 'á': 'á', 'Á': 'Á',
            'e': 'é', 'E': 'É', 'é': 'é', 'É': 'É',
            'i': 'î', 'I': 'Î', 'í': 'î', 'Í': 'Î',
            'o': 'ô', 'O': 'Ô', 'ó': 'ô', 'Ó': 'Ô',
            'u': 'û', 'U': 'Û', 'ú': 'û', 'Ú': 'Û'
        }

        word = match.group(0)
        prefix = match.group(1)
        suffix_vowel = match.group(2)
        suffix_const = match.group(3)

        if word.lower() in list(WORDEND_D_RULES_EXCEPT.keys()):
            return keep_case(word, WORDEND_D_RULES_EXCEPT[word.lower()])
        if any(
            s in prefix for s in (
                'á',
                'é',
                'í',
                'ó',
                'ú',
                'Á',
                'É',
                'Í',
                'Ó',
                'Ú')):
            return prefix + unstressed_rules[suffix_vowel]
        else:
            if suffix_vowel in ('a', 'e', 'A', 'E', 'á', 'é', 'Á', 'É'):
                return prefix + stressed_rules[suffix_vowel]
            else:
                if suffix_const.isupper():
                    return prefix + stressed_rules[suffix_vowel] + 'H'
                else:
                    return prefix + stressed_rules[suffix_vowel] + 'h'

    def replace_s_end_with_case(match):
        repl_rules = {
            'a': 'â', 'A': 'Â', 'á': 'â', 'Á': 'Â',
            'e': 'ê', 'E': 'Ê', 'é': 'ê', 'É': 'Ê',
            'i': 'î', 'I': 'Î', 'í': 'î', 'Í': 'Î',
            'o': 'ô', 'O': 'Ô', 'ó': 'ô', 'Ó': 'Ô',
            'u': 'û', 'U': 'Û', 'ú': 'û', 'Ú': 'Û'
        }

        prefix = match.group(1)
        suffix_vowel = match.group(2)
        suffix_const = match.group(3)
        word = prefix + suffix_vowel + suffix_const

        if word.lower() in list(WORDEND_S_RULES_EXCEPT.keys()):
            return keep_case(word, WORDEND_S_RULES_EXCEPT[word.lower()])
        elif suffix_vowel in ('á', 'é', 'í', 'ó', 'ú', 'Á', 'É', 'Í', 'Ó', 'Ú'):
            if suffix_const.isupper():
                return prefix + repl_rules[suffix_vowel] + 'H'
            else:
                return prefix + repl_rules[suffix_vowel] + 'h'
        else:
            return prefix + repl_rules[suffix_vowel]

    def replace_const_end_with_case(match):
        repl_rules = {
            'a': 'â', 'A': 'Â', 'á': 'â', 'Á': 'Â',
            'e': 'ê', 'E': 'Ê', 'é': 'ê', 'É': 'Ê',
            'i': 'î', 'I': 'Î', 'í': 'î', 'Í': 'Î',
            'o': 'ô', 'O': 'Ô', 'ó': 'ô', 'Ó': 'Ô',
            'u': 'û', 'U': 'Û', 'ú': 'û', 'Ú': 'Û'
        }

        word = match.group(0)
        prefix = match.group(1)
        suffix_vowel = match.group(2)
        suffix_const = match.group(3)

        else_cond = any(
            s in prefix
            for s in ('á', 'é', 'í', 'ó', 'ú', 'Á', 'É', 'Í', 'Ó', 'Ú'))

        if word.lower() in list(WORDEND_CONST_RULES_EXCEPT.keys()):
            return keep_case(word, WORDEND_CONST_RULES_EXCEPT[word.lower()])
        elif else_cond:
            return prefix + repl_rules[suffix_vowel]
        else:
            if suffix_const.isupper():
                return prefix + repl_rules[suffix_vowel] + 'H'
            else:
                return prefix + repl_rules[suffix_vowel] + 'h'

    def replace_eps_end_with_case(match):

        prefix = match.group(1)
        suffix_vowel = match.group(2)
        suffix_const = match.group(3)

        if any(
            s in prefix for s in (
                'á',
                'é',
                'í',
                'ó',
                'ú',
                'Á',
                'É',
                'Í',
                'Ó',
                'Ú')):
            if suffix_vowel.isupper():
                return prefix + 'Ê'
            else:
                return prefix + 'ê'
        else:
            # Leave as it is. There shouldn't be any word with -eps ending
            # withough accent.
            return prefix + suffix_vowel + suffix_const

    def replace_intervowel_d_end_with_case(match):
        prefix = match.group(1)
        suffix_vowel_a = match.group(2)
        suffix_d_char = match.group(3)
        suffix_vowel_b = match.group(4)
        ending_s = match.group('s')

        suffix = suffix_vowel_a + suffix_d_char + suffix_vowel_b + ending_s
        word = prefix + suffix
        else_cond = any(
            s in prefix
            for s in ('á', 'é', 'í', 'ó', 'ú', 'Á', 'É', 'Í', 'Ó', 'Ú'))
        if word.lower() in list(WORDEND_D_INTERVOWEL_RULES_EXCEPT.keys()):
            return keep_case(word,
                             WORDEND_D_INTERVOWEL_RULES_EXCEPT[word.lower()])
        elif not else_cond:
            # Ending word -ada rules
            if suffix.lower() == 'ada':
                if suffix_vowel_b.isupper():
                    return prefix + 'Á'
                else:
                    return prefix + 'á'
            # Ending word -ada rules
            if suffix.lower() == 'adas':
                return prefix + \
                    keep_case(suffix[:2], get_vowel_circumflex(suffix[0]) + 'h')
            # Ending word -ado rules
            elif suffix.lower() == 'ado':
                return prefix + suffix_vowel_a + suffix_vowel_b
            # Ending word -ados -idos -ídos rules
            elif suffix.lower() in ('ados', 'idos', 'ídos'):
                return (
                    prefix
                    + get_vowel_tilde(suffix_vowel_a)
                    + get_vowel_circumflex(suffix_vowel_b))
            # Ending word -ido -ído rules
            elif suffix.lower() in ('ido', 'ído'):
                if suffix_vowel_a.isupper():
                    return prefix + 'Í' + suffix_vowel_b
                else:
                    return prefix + 'í' + suffix_vowel_b
            else:
                return word
        else:
            return word

    # Intervowel /d/ replacements
    text = re.sub(
        r'\b(\w*?)(a|i|í|Í)(d)(o|a)(?P<s>s?)\b',
        replace_intervowel_d_end_with_case,
        text,
        flags=re.IGNORECASE | re.UNICODE)

    text = re.sub(
        r'\b(\w+?)(e)(ps)\b',
        replace_eps_end_with_case,
        text,
        flags=re.IGNORECASE | re.UNICODE)
    text = re.sub(
        r'\b(\w+?)(a|e|i|o|u|á|é|í|ó|ú)(d)\b',
        replace_d_end_with_case,
        text,
        flags=re.IGNORECASE | re.UNICODE)
    text = re.sub(
        r'\b(\w+?)(a|e|i|o|u|á|é|í|ó|ú)(s)\b',
        replace_s_end_with_case,
        text,
        flags=re.IGNORECASE | re.UNICODE)
    text = re.sub(
        r'\b(\w+?)(a|e|i|o|u|á|é|í|ó|ú)(b|c|f|g|j|k|l|p|r|t|x|z)\b',
        replace_const_end_with_case,
        text,
        flags=re.IGNORECASE | re.UNICODE)

    return text


def exception_rules(text):
    """Set of exceptions to the replacement algorithm"""

    def replace_with_case(match):
        word = match.group(1)

        replacement_word = ENDING_RULES_EXCEPTION[word.lower()]
        return keep_case(word, replacement_word)

    text = re.sub(
        r'\b(' +
        '|'.join(
            list(
                ENDING_RULES_EXCEPTION.keys())) +
        r')\b',
        replace_with_case,
        text,
        flags=re.IGNORECASE | re.UNICODE)
    return text


def word_interaction_rules(text):
    """Contractions and other word interaction rules"""

    def replace_with_case(match):
        prefix = match.group(1)
        l_char = match.group(2)
        whitespace_char = match.group(3)
        next_word_char = match.group(4)

        r_char = keep_case(l_char, 'r')
        return prefix + r_char + whitespace_char + next_word_char

    # Rotating word ending /l/ with /r/ if first next word char is non-r
    # consonant
    text = re.sub(
        r'\b(\w*?)(l)(\s)(b|c|ç|d|f|g|h|j|k|l|m|n|ñ|p|q|s|t|v|w|x|y|z)',
        replace_with_case,
        text,
        flags=re.IGNORECASE | re.UNICODE)
    return text

# Main function


def epa(text, vaf=VAF, vvf=VVF, escape_links=False, debug=False):  # noqa: C901
    rules = [
        h_rules,
        x_rules,
        ch_rules,
        gj_rules,
        v_rules,
        ll_rules,
        l_rules,
        psico_pseudo_rules,
        vaf_rules,
        word_ending_rules,
        digraph_rules,
        exception_rules,
        word_interaction_rules
    ]

    if not isinstance(text, str):
        text = str(text, 'utf-8')

    # Do not start transcription if the input is empty
    if not text:
        return text

    def transliterate(text):
        for rule in rules:
            if rule in [x_rules, vaf_rules]:
                text = rule(text, vaf)
            elif rule == gj_rules:
                text = rule(text, vvf)
            else:
                text = rule(text)
            if debug:
                print(rule.__name__ + ' => ' + text)

        return text

    if escape_links:
        # Words in the message not to transliterate
        ignore = to_ignore_re.findall(text)
        # Spanish words in the message to transliterate
        words = to_ignore_re.split(text)

        if not ignore:
            tags = []
            text = text
        else:
            # Replace words to ignore in the transliteration with randints
            tags = list(zip([str(random.randint(1, 999999999))
                             for x in ignore], ignore))
            text = ''.join(reduce(
                lambda x, y: ''.join(x) + ''.join(y), list(zip(words, [x[0] for x in tags]))))  # NOQA: 501
            if len(words) > len(ignore):
                text += words[-1]

        if debug:
            print('escapeLinks => ' + text)
        text_and = transliterate(text)
        for tag in tags:
            text_and = text_and.replace(tag[0], tag[1])
        if debug:
            print('unEscapeLinks => ' + text_and)
        return text_and
    else:
        return transliterate(text)


class AndaluhError(Exception):
    def __init__(self, message, errors):

        # Call the base class constructor with the parameters it needs
        super(AndaluhError, self).__init__(message)

        # Now for your custom code...
        self.errors = errors
