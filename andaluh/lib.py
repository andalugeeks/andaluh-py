#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4
###
# 
# Copyright (c) 2018-2019 Andalugeeks
# Authors:
# - Ksar Feui <a.moreno.losana@gmail.com>
# - J. Félix Ontañón <felixonta@gmail.com>

import re
from exceptions import Exception

from andaluh.defs import  *

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

#TODO: This can be improved to perform replacement in a per character basis
#NOTE: It assumes replacement_word to be already lowercase
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

        if word.lower() in H_RULES_EXCEPT.keys():
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

            return re.sub(ur'(?<!c)(h)(\w?)', replace_with_case, word, flags=re.IGNORECASE)

    # chihuahua => chiguagua
    text = re.sub(ur'(?<!c)(h)(ua)', lambda match: u'g' + match.group(2) if match.group(1).islower() else u'G' + match.group(2), text, flags=re.IGNORECASE|re.UNICODE)
    # cacahuete => cacagûete
    text = re.sub(ur'(?<!c)(h)(u)(e)', lambda match: u'g' + keep_case(match.group(2), u'ü') + match.group(3) if match.group(1).islower() else u'G' + keep_case(match.group(2), u'ü') + match.group(3), text, flags=re.IGNORECASE|re.UNICODE)

    # General /h/ replacements
    text = re.sub(ur'\b(\w*?)(h)(\w*?)\b', replace_with_case, text, flags=re.IGNORECASE)
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
            return prev_char + vaf.upper()*2 + next_char
        else:
            return prev_char + vaf*2 + next_char

    # If the text begins with /ks/
    # Xilófono roto => Çilófono roto
    if text[0] == "X": text = vaf.upper() + text[1:]
    if text[0] == "x": text = vaf + text[1:]

    # If the /ks/ sound is between vowels
    # Axila => Aççila | Éxito => Éççito
    text = re.sub(ur'(a|e|i|o|u|á|é|í|ó|ú)(x)(a|e|i|o|u|á|é|í|ó|ú)', replace_intervowel_with_case, text, flags=re.IGNORECASE|re.UNICODE)

    # Every word starting with /ks/
    text = re.sub(ur'\b(x)', replace_with_case, text, flags=re.IGNORECASE|re.UNICODE)

    return text

def ch_rules(text):
    """Replacement rules for /∫/ (voiceless postalveolar fricative)"""

    text = re.sub(ur'(c)(h)', lambda match: u'x' if match.group(1).islower() else u'X', text, flags=re.IGNORECASE)
    return text

def gj_rules(text, vvf=VVF):
    """Replacing /x/ (voiceless postalveolar fricative) with /h/"""

    def replace_h_with_case(match):
        word = match.group(0)

        if word.lower() in GJ_RULES_EXCEPT.keys():
            return keep_case(word, GJ_RULES_EXCEPT[word.lower()])
        else:
            #TODO: This is an AWFUL way of implementing replacement rules with exceptions. To be fixed.
            word = re.sub(ur'(g|j)(e|i|é|í)', lambda match: vvf + match.group(2) if match.group(1).islower() else vvf.upper() + match.group(2), word, flags=re.IGNORECASE|re.UNICODE)
            word = re.sub(ur'(j)(a|o|u|á|ó|ú)', lambda match: vvf + match.group(2) if match.group(1).islower() else vvf.upper() + match.group(2), word, flags=re.IGNORECASE|re.UNICODE)
            return word

    def replace_g_with_case(match):
        s = match.group('s')
        a = match.group('a')
        b = match.group('b')
        ue = match.group('ue')
        const = match.group('const')

        return s + a + keep_case(b, 'g') + ue + const

    text = re.sub(ur'\b(\w*?)(g|j)(e|i|é|í)(\w*?)\b', replace_h_with_case, text, flags=re.IGNORECASE|re.UNICODE)
    text = re.sub(ur'\b(\w*?)(j)(a|o|u|á|ó|ú)(\w*?)\b', replace_h_with_case, text, flags=re.IGNORECASE|re.UNICODE)

    # GUE,GUI replacement
    text = re.sub(ur'(gu|gU)(e|i|é|í|E|I|É|Í)', ur'g\2', text)
    text = re.sub(ur'(Gu|GU)(e|i|é|í|E|I|É|Í)', ur'G\2', text)

    # GÜE,GÜI replacement
    text = re.sub(ur'(g|G)(ü)(e|i|é|í|E|I|É|Í)', ur'\1u\3', text)
    text = re.sub(ur'(g|G)(Ü)(e|i|é|í|E|I|É|Í)', ur'\1U\3', text)

    # buen / abuel / sabues => guen / aguel / sagues
    # TODO: I've the gut feeling the following two regex can be merged into one.
    text = re.sub(ur'(b)(uen)', lambda match: u'g' + match.group(2) if match.group(1).islower() else u'G' + match.group(2), text, flags=re.IGNORECASE|re.UNICODE)
    text = re.sub(ur'(?P<s>s?)(?P<a>a?)(?<!m)(?P<b>b)(?P<ue>ue)(?P<const>l|s)', replace_g_with_case, text, flags=re.IGNORECASE|re.UNICODE)

    return text

def v_rules(text):
    """Replacing all /v/ (Voiced labiodental fricative) with /b/"""

    def replace_with_case(match):
        word = match.group(0)

        if word.lower() in V_RULES_EXCEPT.keys():
            return keep_case(word, V_RULES_EXCEPT[word.lower()])
        else:
            # NV -> NB -> MB (i.e.: envidia -> embidia)
            word = re.sub(ur'nv', lambda match: keep_case(match.group(0), 'mb'), word, flags=re.IGNORECASE|re.UNICODE)
            word = re.sub(ur'v', ur'b', word)
            word = re.sub(ur'V', ur'B', word)
            return word

    text = re.sub(ur'\b(\w*?)(v)(\w*?)\b', replace_with_case, text, flags=re.IGNORECASE|re.UNICODE)
    return text

def ll_rules(text):
    """Replacing /ʎ/ (digraph ll) with Greek Y for /ʤ/ sound (voiced postalveolar affricate)"""

    def replace_with_case(match):
        word = match.group(0)

        if word.lower() in LL_RULES_EXCEPT.keys():
            return keep_case(word, LL_RULES_EXCEPT[word.lower()])
        else:
            return re.sub(ur'(l)(l)', lambda match: 'Y' if match.group(1).isupper() else 'y', word, flags=re.IGNORECASE)

    text = re.sub(ur'\b(\w*?)(l)(l)(\w*?)\b', replace_with_case, text, flags=re.IGNORECASE)
    return text

def l_rules(text):
    """Rotating /l/ with /r/"""

    text = re.sub(
        ur'(l)(b|c|ç|Ç|g|s|d|f|g|h|k|m|p|q|r|t|x|z)',
        lambda match: 'r' + match.group(2) if match.group(1).islower() else 'R' + match.group(2),
        text, flags=re.IGNORECASE
    )
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

def vaf_rules(text, vaf=VAF):
    """Replacing Voiceless alveolar fricative (vaf) /s/ /θ/ with EPA's ç/Ç"""

    def replace_with_case(match):
        l_char = match.group(1)
        next_char = match.group(2)

        if l_char.islower():
            return vaf + next_char
        else:
            return vaf.upper() + next_char

    text = re.sub(ur'(z|s)(a|e|i|o|u|á|é|í|ó|ú|â|ê|î|ô|û)', replace_with_case, text, flags=re.IGNORECASE|re.UNICODE)
    text = re.sub(ur'(c)(e|i|é|í|ê|î)', replace_with_case, text, flags=re.IGNORECASE|re.UNICODE)

    return text

def digraph_rules(text):
    """Replacement of consecutive consonant with EPA VAF"""

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

    def replace_bdnr_s_with_case(match):
        vowel_char = match.group(1)
        cons_char = match.group(2)
        s_char = match.group(3)
        digraph_char = match.group(4)

        if cons_char.lower() + s_char.lower() == u'rs':
            return vowel_char + cons_char + digraph_char*2
        else:
            return get_vowel_circumflex(vowel_char) + digraph_char*2

    def replace_transpost_with_case(match):
        init_char = match.group(1)
        vowel_char = match.group(2)
        cons_char = match.group(4)

        if cons_char.lower() == u'l':
            return init_char + get_vowel_circumflex(vowel_char) + cons_char + u'-' + cons_char
        else:
            return init_char + get_vowel_circumflex(vowel_char) + cons_char*2

    def replace_l_with_case(match):
        vowel_char = match.group(1)
        digraph_char = match.group(3)

        return get_vowel_circumflex(vowel_char) + digraph_char + u'-' + digraph_char

    def replace_digraph_with_case(match):
        vowel_char = match.group(1)
        to_drop_char, digraph_char = match.group(2)

        return get_vowel_circumflex(vowel_char) + digraph_char*2

    # intersticial / solsticio / superstición / cárstico => interttiçiâh / çorttiçio / çuperttiçión / cárttico
    text = re.sub(ur'(a|e|i|o|u|á|é|í|ó|ú)(l|r)(s)(t)', replace_lstrst_with_case, text, flags=re.IGNORECASE)
    # aerotransporte => aerotrâpporte | translado => trâl-lado | transcendente => trâççendente | postoperatorio => pôttoperatorio | postpalatal => pôppalatal
    text = re.sub(ur'(tr|p)(a|o)(ns|st)(b|c|ç|Ç|d|f|g|h|j|k|l|m|n|p|q|s|t|v|w|x|y|z)', replace_transpost_with_case, text, flags=re.IGNORECASE|re.UNICODE)
    # abstracto => âttrâtto | adscrito => âccrito | perspectiva => pêrppêttiba
    text = re.sub(ur'(a|e|i|o|u|á|é|í|ó|ú)(b|d|n|r)(s)(b|c|ç|Ç|d|f|g|h|j|k|l|m|n|p|q|s|t|v|w|x|y|z)', replace_bdnr_s_with_case, text, flags=re.IGNORECASE|re.UNICODE)
    # atlántico => âl-lántico | orla => ôl-la | adlátere => âl-látere | tesla => têl-la ...
    text = re.sub(ur'(a|e|i|o|u|á|é|í|ó|ú)(d|j|r|s|t|x|z)(l)', replace_l_with_case, text, flags=re.IGNORECASE|re.UNICODE)

    # General digraph rules.
    text = re.sub(ur'(a|e|i|o|u|á|é|í|ó|ú)(' + u'|'.join(DIGRAPHS) + ')', replace_digraph_with_case, text, flags=re.IGNORECASE|re.UNICODE)

    return text

def word_ending_rules(text):

    def replace_d_end_with_case(match):
        unstressed_rules = {
            u'a':u'â', u'A':u'Â', u'á':u'â', u'Á':u'Â',
            u'e':u'ê', u'E':u'Ê', u'é':u'ê', u'É':u'Ê',
            u'i':u'î', u'I':u'Î', u'í':u'î', u'Í':u'Î',
            u'o':u'ô', u'O':u'Ô', u'ó':u'ô', u'Ó':u'Ô',
            u'u':u'û', u'U':u'Û', u'ú':u'û', u'Ú':u'Û'
        }

        stressed_rules = {
            u'a':u'á', u'A':u'Á', u'á':u'á', u'Á':u'Á',
            u'e':u'é', u'E':u'É', u'é':u'é', u'É':u'É',
            u'i':u'î', u'I':u'Î', u'í':u'î', u'Í':u'Î',
            u'o':u'ô', u'O':u'Ô', u'ó':u'ô', u'Ó':u'Ô',
            u'u':u'û', u'U':u'Û', u'ú':u'û', u'Ú':u'Û'
        }

        word = match.group(0)
        prefix = match.group(1)
        suffix_vowel = match.group(2)
        suffix_const = match.group(3)

        if word.lower() in WORDEND_D_RULES_EXCEPT.keys():
            return keep_case(word, WORDEND_D_RULES_EXCEPT[word.lower()])
        if any(s in prefix for s in (u'á',u'é',u'í',u'ó',u'ú',u'Á',u'É',u'Í',u'Ó',u'Ú')):
            return prefix + unstressed_rules[suffix_vowel]
        else:
            if suffix_vowel in (u'a',u'e',u'A',u'E',u'á',u'é',u'Á',u'É'):
                return prefix + stressed_rules[suffix_vowel]
            else:
                if suffix_const.isupper():
                    return prefix + stressed_rules[suffix_vowel] + 'H'
                else:
                    return prefix + stressed_rules[suffix_vowel] + 'h'

    def replace_s_end_with_case(match):
        repl_rules = {
            u'a':u'â', u'A':u'Â', u'á':u'â', u'Á':u'Â',
            u'e':u'ê', u'E':u'Ê', u'é':u'ê', u'É':u'Ê',
            u'i':u'î', u'I':u'Î', u'í':u'î', u'Í':u'Î',
            u'o':u'ô', u'O':u'Ô', u'ó':u'ô', u'Ó':u'Ô',
            u'u':u'û', u'U':u'Û', u'ú':u'û', u'Ú':u'Û'
        }

        prefix = match.group(1)
        suffix_vowel = match.group(2)
        suffix_const = match.group(3)
        word = prefix + suffix_vowel + suffix_const

        if word.lower() in WORDEND_S_RULES_EXCEPT.keys():
            return keep_case(word, WORDEND_S_RULES_EXCEPT[word.lower()])
        elif suffix_vowel in (u'á',u'é',u'í',u'ó',u'ú',u'Á',u'É',u'Í',u'Ó',u'Ú'):
            if suffix_const.isupper():
                return prefix + repl_rules[suffix_vowel] + 'H'
            else:
                return prefix + repl_rules[suffix_vowel] + 'h'
        else:
            return prefix + repl_rules[suffix_vowel]

    def replace_const_end_with_case(match):
        repl_rules = {
            u'a':u'â', u'A':u'Â', u'á':u'â', u'Á':u'Â',
            u'e':u'ê', u'E':u'Ê', u'é':u'ê', u'É':u'Ê',
            u'i':u'î', u'I':u'Î', u'í':u'î', u'Í':u'Î',
            u'o':u'ô', u'O':u'Ô', u'ó':u'ô', u'Ó':u'Ô',
            u'u':u'û', u'U':u'Û', u'ú':u'û', u'Ú':u'Û'
        }

        word = match.group(0)
        prefix = match.group(1)
        suffix_vowel = match.group(2)
        suffix_const = match.group(3)

        if word.lower() in WORDEND_CONST_RULES_EXCEPT.keys():
            return keep_case(word, WORDEND_CONST_RULES_EXCEPT[word.lower()])
        elif any(s in prefix for s in (u'á',u'é',u'í',u'ó',u'ú',u'Á',u'É',u'Í',u'Ó',u'Ú')):
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

        if any(s in prefix for s in (u'á',u'é',u'í',u'ó',u'ú',u'Á',u'É',u'Í',u'Ó',u'Ú')):
            if suffix_vowel.isupper():
                return prefix + u'Ê'
            else:
                return prefix + u'ê'
        else:
            # Leave as it is. There shouldn't be any word with -eps ending withough accent.
            return prefix + suffix_vowel + suffix_const

    def replace_intervowel_d_end_with_case(match):
        prefix = match.group(1)
        suffix_vowel_a = match.group(2)
        suffix_d_char = match.group(3)
        suffix_vowel_b = match.group(4)
        ending_s = match.group('s')

        suffix = suffix_vowel_a + suffix_d_char + suffix_vowel_b + ending_s
        word = prefix + suffix

        if word.lower() in WORDEND_D_INTERVOWEL_RULES_EXCEPT.keys():
            return keep_case(word, WORDEND_D_INTERVOWEL_RULES_EXCEPT[word.lower()])
        elif not any(s in prefix for s in (u'á',u'é',u'í',u'ó',u'ú',u'Á',u'É',u'Í',u'Ó',u'Ú')):
            # Ending word -ada rules
            if suffix.lower() == u'ada':
                if suffix_vowel_b.isupper():
                    return prefix + u'Á'
                else:
                    return prefix + u'á'
            # Ending word -ada rules
            if suffix.lower() == u'adas':
                return prefix + keep_case(suffix[:2], get_vowel_circumflex(suffix[0]) + u'h')
            # Ending word -ado rules
            elif suffix.lower() == u'ado':
                return prefix + suffix_vowel_a + suffix_vowel_b
            # Ending word -ados -idos -ídos rules
            elif suffix.lower() in (u'ados', u'idos', u'ídos'):
                return prefix + get_vowel_tilde(suffix_vowel_a) + get_vowel_circumflex(suffix_vowel_b)
            # Ending word -ido -ído rules
            elif suffix.lower() in (u'ido', u'ído'):
                if suffix_vowel_a.isupper():
                    return prefix + u'Í' + suffix_vowel_b
                else:
                    return prefix + u'í' + suffix_vowel_b
            else:
                return word
        else:
            return word

    # Intervowel /d/ replacements
    text = re.sub(ur'\b(\w*?)(a|i|í|Í)(d)(o|a)(?P<s>s?)\b', replace_intervowel_d_end_with_case, text, flags=re.IGNORECASE|re.UNICODE)

    text = re.sub(ur'\b(\w+?)(e)(ps)\b', replace_eps_end_with_case, text, flags=re.IGNORECASE|re.UNICODE)
    text = re.sub(ur'\b(\w+?)(a|e|i|o|u|á|é|í|ó|ú)(d)\b', replace_d_end_with_case, text, flags=re.IGNORECASE|re.UNICODE)
    text = re.sub(ur'\b(\w+?)(a|e|i|o|u|á|é|í|ó|ú)(s)\b', replace_s_end_with_case, text, flags=re.IGNORECASE|re.UNICODE)
    text = re.sub(ur'\b(\w+?)(a|e|i|o|u|á|é|í|ó|ú)(b|c|f|g|j|k|l|p|r|t|x|z)\b', replace_const_end_with_case, text, flags=re.IGNORECASE|re.UNICODE)

    return text

def exception_rules(text):
    """Set of exceptions to the replacement algorithm"""

    def replace_with_case(match):
        word = match.group(1)

        replacement_word = ENDING_RULES_EXCEPTION[word.lower()]
        return keep_case(word, replacement_word)

    text = re.sub(ur'\b(' + u'|'.join(ENDING_RULES_EXCEPTION.keys()) + ur')\b', replace_with_case, text, flags=re.IGNORECASE|re.UNICODE)
    return text

def word_interaction_rules(text):
    """Contractions and other word interaction rules"""

    def replace_with_case(match):
        prefix = match.group(1)
        l_char = match.group(2)
        whitespace_char = match.group(3)
        next_word_char = match.group(4)

        r_char = keep_case(l_char, u'r')
        return prefix + r_char + whitespace_char + next_word_char

    # Rotating word ending /l/ with /r/ if first next word char is non-r consonant
    text = re.sub(ur'\b(\w*?)(l)(\s)(b|c|ç|d|f|g|h|j|k|l|m|n|ñ|p|q|s|t|v|w|x|y|z)', replace_with_case, text, flags=re.IGNORECASE|re.UNICODE)
    return text

# Main function
def epa(text, vaf=VAF, vvf=VVF, debug=False):
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

    if type(text) != unicode:
        text = unicode(text, 'utf-8')

    # Do not start transcription if the input is empty
    if not text:
        return text

    for rule in rules:
        if rule in [x_rules, vaf_rules]:
            text = rule(text, vaf)
        elif rule == gj_rules:
            text = rule(text, vvf)
        else:
            text = rule(text)
        if debug: print rule.func_name + ' => ' + text

    return text

class AndaluhError(Exception):
    def __init__(self, message, errors):

        # Call the base class constructor with the parameters it needs
        super(AndaluhError, self).__init__(message)

        # Now for your custom code...
        self.errors = errors
