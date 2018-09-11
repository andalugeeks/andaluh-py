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

    if vowel and vowel in VOWELS_ALL_NOTILDE:
        i = VOWELS_ALL_NOTILDE.find(vowel) + 5
        return VOWELS_ALL_NOTILDE[i: i+1][0]
    elif vowel and vowel in VOWELS_ALL_TILDE:
        i = VOWELS_ALL_TILDE.find(vowel) + 5
        return VOWELS_ALL_TILDE[i: i+1][0]
    else:
        raise EPAError('Not a vowel', vowel)

def intervowel_circumflex_sub(match):
    prev_char = match.group(1)
    consonant_char = match.group(2)
    next_char = match.group(3)

    prev_char = get_vowel_circumflex(prev_char)

    if consonant_char.isupper(): 
        return prev_char + VAF_UP*2 + next_char
    else: 
        return prev_char + VAF*2 + next_char

# EPA replacement functions
def h_rules(text):
    """Supress mute /h/"""

    text = re.sub(ur'(?<!c)h', '', text, flags=re.IGNORECASE)
    return text

#TODO: When there's TILDE, do not replace with circumflex
#TODO: Review why "Xilofono" crashes
def x_rules(text):
    """Replacement rules for /ks/ with EPA VAF"""

    if text[0] == "X": text[0] = VAF.upper()
    if text[0] == "x": text[0] = VAF

    # Try substitution for all combination of vowels upper/lower and tildes
    for pair in [(VOWELS, VOWELS), (VOWELS_TILDE, VOWELS), (VOWELS_TILDE_UP, VOWELS), (VOWELS, VOWELS_TILDE), (VOWELS, VOWELS_TILDE_UP)]:
        text = re.sub(ur'([' + pair[0] + '])(x)([' + pair[1] + '])', intervowel_circumflex_sub, text, flags=re.IGNORECASE)

    return text

def ch_rules(text):
    """Replacement rules for /∫/ (voiceless postalveolar fricative)"""

    text = text.replace(ur'ch', ur'x')
    text = text.replace(ur'Ch', ur'X')
    text = text.replace(ur'CH', ur'X')
    text = text.replace(ur'cH', ur'x') # weird, but who knows?
    return text

#TODO: when 'j' is last character of word the rules does not affect.
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
    text = vaf_rules(text)

    return text

class EPAError(Exception):
    def __init__(self, message, errors):

        # Call the base class constructor with the parameters it needs
        super(EPAError, self).__init__(message)

        # Now for your custom code...
        self.errors = errors