#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4
###
# 
# Copyright (c) 2018 EPA
# Authors : J. Félix Ontañón <felixonta@gmail.com>

import re
from exceptions import Exception

VOWELS = u'aeiou'
VOWELS_TILDE = u'áéíóú'
VOWELS_CIRCUMFLEX = u'âêîôû'
VOWELS_UP = u'AEIOU'
VOWELS_TILDE_UP = u'ÁÉÍÓÚ' 
VOWELS_CIRCUMFLEX_UP = u'ÂÊÎÔÛ'

# Pre calculation of vowel groups and its variants with accents. Useful for further search & replacement
VOWELS_ALL = VOWELS + VOWELS_TILDE + VOWELS_CIRCUMFLEX + VOWELS_UP + VOWELS_TILDE_UP + VOWELS_CIRCUMFLEX_UP
VOWELS_ALL_NOTILDE = VOWELS + VOWELS_CIRCUMFLEX + VOWELS_UP + VOWELS_CIRCUMFLEX_UP
VOWELS_ALL_TILDE = VOWELS_TILDE + VOWELS_CIRCUMFLEX + VOWELS_TILDE_UP + VOWELS_CIRCUMFLEX_UP

# EPA character for Voiceless alveolar fricative /s/ https://en.wikipedia.org/wiki/Voiceless_alveolar_fricative
VAF = u'ç'
VAF_UP = u'Ç'

# Auxiliary functions
def get_vowel_circumflex(vowel):

    # If no tilde, replace with circumflex
    if vowel and vowel in VOWELS_ALL_NOTILDE:
        i = VOWELS_ALL_NOTILDE.find(vowel) + 5
        return VOWELS_ALL_NOTILDE[i: i+1][0]

    # If vowel with tilde, leave it as it is
    elif vowel and vowel in VOWELS_ALL_TILDE:
        return vowel

    # You shouldn't call this method with a non vowel
    else:
        raise EPAError('Not a vowel', vowel)

# EPA replacement functions
def h_rules(text):
    """Supress mute /h/"""

    text = re.sub(ur'(?<!c)h', '', text, flags=re.IGNORECASE)
    return text

def x_rules(text):
    """Replacement rules for /ks/ with EPA VAF"""

    def replace_with_case(match):
        whitespaces = match.group(1)
        x_char = match.group(2)

        if x_char.islower():
            return whitespaces + VAF
        else:
            return whitespaces + VAF_UP

    def replace_intervowel_with_case(match):
        prev_char = match.group(1)
        x_char = match.group(2)
        next_char = match.group(3)

        prev_char = get_vowel_circumflex(prev_char)

        if x_char.isupper():
            return prev_char + VAF_UP*2 + next_char
        else:
            return prev_char + VAF*2 + next_char

    # If the text begins with /ks/
    if text[0] == "X": text = VAF_UP + text[1:]
    if text[0] == "x": text = VAF + text[1:]

    # If the /ks/ sound is between vowels
    text = re.sub(ur'(a|e|i|o|u|á|é|í|ó|ú|Á|É|Í|Ó|Ú)(x)(a|e|i|o|u|á|é|í|ó|ú|Á|É|Í|Ó|Ú)', replace_intervowel_with_case, text, flags=re.IGNORECASE)

    # Every word starting with /ks/
    text = re.sub(ur'([\W]+)(x|X)', replace_with_case, text, flags=re.IGNORECASE)

    return text

def ch_rules(text):
    """Replacement rules for /∫/ (voiceless postalveolar fricative)"""

    text = text.replace(ur'ch', ur'x')
    text = text.replace(ur'Ch', ur'X')
    text = text.replace(ur'CH', ur'X')
    text = text.replace(ur'cH', ur'x') # weird, but who knows?
    return text

def gj_rules(text):
    """Replacing /x/ (voiceless postalveolar fricative) with /h/"""
    # G,J + vowel replacement
    text = re.sub(ur'(g|j)(e|i|é|í|E|I|É|Í)', ur'h\2', text)
    text = re.sub(ur'(G|J)(e|i|é|í|E|I|É|Í)', ur'H\2', text)
    text = re.sub(ur'(j)(a|o|u|á|ó|ú|A|O|U|Á|Ó|Ú)', ur'h\2', text)
    text = re.sub(ur'(J)(a|o|u|á|ó|ú|A|O|U|Á|Ó|Ú)', ur'H\2', text)

    # GUE,GUI replacement
    text = re.sub(ur'(gu|gU)(e|i|é|í|E|I|É|Í)', ur'g\2', text)
    text = re.sub(ur'(Gu|GU)(e|i|é|í|E|I|É|Í)', ur'G\2', text)

    # GÜE,GÜI replacement
    text = re.sub(ur'(g|G)(ü)(e|i|é|í|E|I|É|Í)', ur'\1u\3', text)
    text = re.sub(ur'(g|G)(Ü)(e|i|é|í|E|I|É|Í)', ur'\1U\3', text)

    return text

def v_rules(text):
    """Replacing all /v/ (Voiced labiodental fricative) with /b/"""

    def replace_with_case(match):
        n_char = match.group(1)
        v_char = match.group(2)

        if n_char.islower() and v_char.islower():
            return 'mb'
        if n_char.isupper() and v_char.isupper():
            return 'MB'
        if n_char.isupper() and v_char.islower():
            return 'Mb'
        else: 
            return 'mB'

    # NV -> NB -> MB (i.e.: envidia -> embidia)
    text = re.sub(ur'(n)(v)', replace_with_case, text, flags=re.IGNORECASE)

    # v -> b
    text = re.sub(ur'v', ur'b', text)
    text = re.sub(ur'V', ur'B', text)

    return text

def ll_rules(text):
    """Replacing /ʎ/ (digraph ll) with Greek Y for /ʤ/ sound (voiced postalveolar affricate)"""

    def replace_with_case(match):
        l1_char = match.group(1)

        if l1_char.islower():
            return 'y'
        else:
            return 'Y'

    text = re.sub(ur'(l)(l)', replace_with_case, text, flags=re.IGNORECASE)
    return text

def l_rules(text):
    """Rotating /l/ with /r/"""

    def replace_with_case(match):
        l_char = match.group(1)
        next_char = match.group(2)

        if l_char.islower():
            return 'r' + next_char
        else: 
            return 'R' + next_char

    text = re.sub(ur'(l)(b|c|g|s|d|f|g|h|m|n|p|q|r|t|x)', replace_with_case, text, flags=re.IGNORECASE)
    return text

def psico_pseudo_rules(text):
    """Drops /p/ for pseudo- or psico- prefixes"""

    def replace_psicpseud_with_case(match):
        ps_syllable = match.group(1)

        if ps_syllable[0] == u'p':
            return ps_syllable[1:]
        else:
            return ps_syllable[1].upper() + ps_syllable[2:]

    text = re.sub(ur'(psic|pseud)', replace_psicpseud_with_case, text, flags=re.IGNORECASE)
    return text

def vaf_rules(text):
    """Replacing Voiceless alveolar fricative (vaf) /s/ /θ/ with EPA's ç/Ç"""

    def replace_with_case(match):
        l_char = match.group(1)
        next_char = match.group(2)

        if l_char.islower():
            return VAF + next_char
        else:
            return VAF_UP + next_char

    text = re.sub(ur'(z|s)(a|e|i|o|u|á|é|í|ó|ú|Á|É|Í|Ó|Ú)', replace_with_case, text, flags=re.IGNORECASE)
    text = re.sub(ur'(c)(e|i|é|í)', replace_with_case, text, flags=re.IGNORECASE)

    return text

def digraph_rules(text):
    """Replacement of consecutive consonant with EPA VAF"""

    def replace_mn_with_case(match):
        vowel_char = match.group(1)
        n_char = match.group(3)

        return get_vowel_circumflex(vowel_char) + n_char*2

    def replace_nm_with_case(match):
        vowel_char = match.group(1)
        m_char = match.group(3)

        return vowel_char + m_char*2

    def replace_lstrst_with_case(match):
        vowel_char = match.group(1)
        lr_char = match.group(2)
        t_char = match.group(4)

        if lr_char == u'l':
            lr_char == 'r'
        elif lr_char == u'L':
            lr_char == 'R'
        else:
            pass

        return vowel_char + lr_char + t_char*2

    def replace_abs_with_case(match):
        vowel_char = match.group(1)
        cons_char = match.group(3)

        return get_vowel_circumflex(vowel_char) + cons_char*2

    def replace_trans_with_case(match):
        tr_char = match.group(1)
        vowel_char = match.group(2)
        cons_char = match.group(4)

        return tr_char + get_vowel_circumflex(vowel_char) + cons_char*2

    def replace_digraph_with_case(match):
        vowel_char = match.group(1)
        to_drop_char = match.group(2)
        digraph_char = match.group(3)

        # Digraph exceptions
        if (to_drop_char + digraph_char).lower() in (u'bl', u'cl', u'fl', u'gl', u'pl', u'br', u'cr', u'dr', u'fr', u'pr', u'tr'):
            return vowel_char + to_drop_char + digraph_char
        # Double 'l' digraphs => 'l-l'
        elif digraph_char.lower() == u'l':
            return get_vowel_circumflex(vowel_char) + digraph_char + u'-' + digraph_char
        # General digraph rules applies
        else:
            return get_vowel_circumflex(vowel_char) + digraph_char*2

    # amnesia => ânneçia.
    text = re.sub(ur'(a|e|i|o|u|á|é|í|ó|ú|Á|É|Í|Ó|Ú)(m)(n)', replace_mn_with_case, text, flags=re.IGNORECASE)
    # conmemorar => commemorâh
    text = re.sub(ur'(a|e|i|o|u|á|é|í|ó|ú|Á|É|Í|Ó|Ú)(n)(m)', replace_nm_with_case, text, flags=re.IGNORECASE)
    # intersticial / solsticio / superstición / cárstico => interttiçiâh / çorttiçio / çuperttiçión / cárttico
    text = re.sub(ur'(a|e|i|o|u|á|é|í|ó|ú|Á|É|Í|Ó|Ú)(l|r)(s)(t)', replace_lstrst_with_case, text, flags=re.IGNORECASE)
    # abstracto => âttrâtto
    text = re.sub(ur'(a)(bs)([b-df-hj-np-tv-xz])', replace_abs_with_case, text, flags=re.IGNORECASE)
    # transporte => Trâpporte
    text = re.sub(ur'(tr)(a)(ns)([b-df-hj-np-tv-xz])', replace_trans_with_case, text, flags=re.IGNORECASE)

    # General digraph rules
    text = re.sub(ur'(a|e|i|o|u|á|é|í|ó|ú|Á|É|Í|Ó|Ú)(b|c|d|f|g|j|p|s|t|x|z)(b|c|ç|d|f|g|h|l|m|n|p|q|r|t|x|y)', replace_digraph_with_case, text, flags=re.IGNORECASE)

    return text

def word_ending_rules(text):

    def replace_d_end_with_case(match):
        stressed_rules = {
            u'a':u'â', u'e':u'ê', u'A':u'Â', u'E':u'Ê',
            u'i':u'î', u'o':u'ô', u'u':u'û', u'I':u'Î', u'O':u'Ô', u'U':u'Û'
        }
        unstressed_rules = {
            u'ad':u'á', u'aD':u'á', u'ed':u'é', u'eD':u'é',
            u'AD':u'Á', u'Ad':u'Á', u'ED':u'É', u'Ed':u'É',
            u'id':u'îh', u'od':u'ôh', u'ud':u'ûh',
            u'iD':u'îH', u'oD':u'ôH', u'uD':u'ûH',
            u'ID':u'ÎH', u'OD':u'ÔH', u'UD':u'ÛH',
            u'Id':u'Îh', u'Od':u'Ôh', u'Ud':u'Ûh'
        }

        word = match.group(0)
        prefix = match.group(1)
        suffix = match.group(2)

        if any(s in word for s in (u'á',u'é',u'í',u'ó',u'ú',u'Á',u'É',u'Í',u'Ó',u'Ú')):
            return prefix + stressed_rules[suffix[0]]
        else:
            return prefix + unstressed_rules[suffix]

    def replace_lzr_end_with_case(match):
        repl_rules = {
            u'a':u'â', u'e':u'ê', u'i':u'î', u'o':u'ô', u'u':u'û',
            u'A':u'Â', u'E':u'Ê',u'I':u'Î', u'O':u'Ô', u'U':u'Û'
        }

        word = match.group(0)
        prefix = match.group(1)
        suffix_vowel = match.group(2)
        suffix_const = match.group(3)

        if any(s in word for s in (u'á',u'é',u'í',u'ó',u'ú',u'Á',u'É',u'Í',u'Ó',u'Ú')):
            return prefix + repl_rules[suffix_vowel]
        else:
            if suffix_const.isupper():
                return prefix + repl_rules[suffix_vowel] + 'H'
            else:
                return prefix + repl_rules[suffix_vowel] + 'h'

    def replace_s_end_with_case(match):
        repl_rules = {
            u'a':u'â', u'e':u'ê', u'i':u'î', u'o':u'ô', u'u':u'û',
            u'A':u'Â', u'E':u'Ê',u'I':u'Î', u'O':u'Ô', u'U':u'Û',
            u'á':u'â', u'é':u'ê', u'í':u'î', u'ó':u'ô', u'ú':u'û',
            u'Á':u'Â', u'É':u'Ê',u'Í':u'Î', u'Ó':u'Ô', u'Ú':u'Û'
        }

        prefix = match.group(1)
        suffix_vowel = match.group(2)
        suffix_const = match.group(3)

        if suffix_vowel in (u'á',u'é',u'í',u'ó',u'ú',u'Á',u'É',u'Í',u'Ó',u'Ú'):
            if suffix_const.isupper():
                return prefix + repl_rules[suffix_vowel] + 'H'
            else:
                return prefix + repl_rules[suffix_vowel] + 'h'
        else:
            return prefix + repl_rules[suffix_vowel]

    text = re.sub(ur'\b(\w+?)(ad|ed|id|od|ud)\b', replace_d_end_with_case, text, flags=re.IGNORECASE|re.UNICODE)
    text = re.sub(ur'\b(\w+?)(a|e|i|o|u|á|é|í|ó|ú|Á|É|Í|Ó|Ú)(s)\b', replace_s_end_with_case, text, flags=re.IGNORECASE|re.UNICODE)
    text = re.sub(ur'\b(\w+?)(a|e|i|o|u)(l|z|r)\b', replace_lzr_end_with_case, text, flags=re.IGNORECASE|re.UNICODE)

    return text

# Main function
def cas_to_epa(text):
    text = unicode(text, 'utf-8')
    text = h_rules(text)
    text = x_rules(text)
    text = ch_rules(text)
    text = gj_rules(text)
    text = v_rules(text)
    text = ll_rules(text)
    text = l_rules(text)
    text = psico_pseudo_rules(text)
    text = vaf_rules(text)
    text = digraph_rules(text)
    text = word_ending_rules(text)

    return text

class EPAError(Exception):
    def __init__(self, message, errors):

        # Call the base class constructor with the parameters it needs
        super(EPAError, self).__init__(message)

        # Now for your custom code...
        self.errors = errors