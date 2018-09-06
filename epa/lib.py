#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4
###
# 
# Copyright (c) 2018 EPA
# Authors : J. Félix Ontañón <felixonta@gmail.com>

import re
from exceptions import Exception

# Vowels and its variants with accents
VOWELS = 'aeiou'
VOWELS_TILDE = 'áéíóú'
VOWELS_CIRCUMFLEX = 'âêîôû'
VOWELS_UP = 'AEIOU'
VOWELS_TILDE_UP = 'ÁÉÍÓÚ'
VOWELS_CIRCUMFLEX_UP = 'ÂÊÎÔÛ'

# Pre calculation of vowel groups and its variants with accents. Useful for further search & replacement
VOWELS_ALL = VOWELS + VOWELS_TILDE + VOWELS_CIRCUMFLEX + VOWELS_UP + VOWELS_TILDE_UP + VOWELS_CIRCUMFLEX_UP
VOWELS_ALL_NOTILDE = VOWELS + VOWELS_CIRCUMFLEX + VOWELS_UP + VOWELS_CIRCUMFLEX_UP
VOWELS_ALL_TILDE = VOWELS_TILDE + VOWELS_CIRCUMFLEX + VOWELS_TILDE_UP + VOWELS_CIRCUMFLEX_UP

# Voiceless alveolar fricative /s/ https://en.wikipedia.org/wiki/Voiceless_alveolar_fricative
VAF = 'ç'
VAF_UP = 'Ç'

# Auxiliary functions
def get_vowel_circumflex(vowel):
    if vowel in VOWELS_ALL_NOTILDE:
        i = VOWELS_ALL_NOTILDE.find(vowel) + 6
        return VOWELS_ALL_NOTILDE[i: i+2]
    elif vowel in VOWELS_ALL_TILDE:
        i = VOWELS_ALL_TILDE.find(vowel) + 10
        return VOWELS_ALL_TILDE[i: i+1]
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
    """Supress mute 'h'"""
    text = re.sub(r'(?<!c)h', '', text)
    text = re.sub(r'(?<!C)H', '', text)
    return text

def x_rules(text):
    if text[0] == "X": text[0] = VAF.upper()
    if text[0] == "x": text[0] = VAF
    # text = re.sub(r'([aeiou])(x)([aeiou])', r'\1çç\3', text)

    # Try substitution for all combination of vowels upper/lower and tildes
    for pair in [(VOWELS, VOWELS), (VOWELS_TILDE, VOWELS), (VOWELS_TILDE_UP, VOWELS), (VOWELS, VOWELS_TILDE), (VOWELS, VOWELS_TILDE_UP)]:
        new_text = re.sub(r'([' + pair[0] + '])(x)([' + pair[1] + '])', intervowel_circumflex_sub, text, flags=re.IGNORECASE)
        
        # If a substitution was done, there's no need to continue trying
        if new_text != text: 
            text = new_text
            break
        else:
            text = new_text

    return text

# Main function
def cas_to_epa(text):
    # text = text.replace('c', 'ç').replace('C', 'Ç').replace('s', 'ç').replace('S', 'Ç')
    # text = text.replace('s', 'ç').replace('S', 'Ç')

    text = h_rules(text)
    text = x_rules(text)
    return text

class EPAError(Exception):
    def __init__(self, message, errors):

        # Call the base class constructor with the parameters it needs
        super(EPAError, self).__init__(message)

        # Now for your custom code...
        self.errors = errors