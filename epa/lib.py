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

# Digraphs producers. (vowel)(const)(const) that triggers the general digraph rule
DIGRAPHS = [
    u"bb", u"bc", u"bç", u"bÇ", u"bd", u"bf", u"bg", u"bh", u"bm", u"bn", u"bp", u"bq", u"bt", u"bx", u"by", u"cb", u"cc",
    u"cç", u"cÇ", u"cd", u"cf", u"cg", u"ch", u"cm", u"cn", u"cp", u"cq", u"ct", u"cx", u"cy",
    u"db", u"dc", u"dç", u"dÇ", u"dd", u"df", u"dg", u"dh", u"dl", u"dm", u"dn", u"dp", u"dq", u"dt", u"dx", u"dy",
    u"fb", u"fc", u"fç", u"fÇ", u"fd", u"ff", u"fg", u"fh", u"fm", u"fn", u"fp", u"fq", u"ft", u"fx", u"fy",
    u"gb", u"gc", u"gç", u"gÇ", u"gd", u"gf", u"gg", u"gh", u"gm", u"gn", u"gp", u"gq", u"gt", u"gx", u"gy",
    u"jb", u"jc", u"jç", u"jÇ", u"jd", u"jf", u"jg", u"jh", u"jl", u"jm", u"jn", u"jp", u"jq", u"jr", u"jt", u"jx", u"jy",
    u"lb", u"lc", u"lç", u"lÇ", u"ld", u"lf", u"lg", u"lh", u"ll", u"lm", u"ln", u"lp", u"lq", u"lr", u"lt", u"lx", u"ly",
    u"mm", u'mn',
    u'nm', u'nn',
    u"pb", u"pc", u"pç", u"pÇ", u"pd", u"pf", u"pg", u"ph", u"pm", u"pn", u"pp", u"pq", u"pt", u"px", u"py",
    u"rn",
    u"sb", u"sc", u"sç", u"sÇ", u"sd", u"sf", u"sg", u"sh", u"sk", u"sl", u"sm", u"sn", u"sñ", u"sp", u"sq", u"sr", u"st", u"sx", u"sy",
    u"tb", u"tc", u"tç", u"tÇ", u"td", u"tf", u"tg", u"th", u"tl", u"tm", u"tn", u"tp", u"tq", u"tt", u"tx", u"ty",
    u"xb", u"xc", u"xç", u"xÇ", u"xd", u"xf", u"xg", u"xh", u"xl", u"xm", u"xn", u"xp", u"xq", u"xr", u"xt", u"xx", u"xy",
    u"zb", u"zc", u"zç", u"zÇ", u"zd", u"zf", u"zg", u"zh", u"zl", u"zm", u"zn", u"zp", u"zq", u"zr", u"zt", u"zx", "zy"
]

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
        x_char = match.group(1)

        if x_char.islower():
            return VAF
        else:
            return VAF_UP

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
    # Xilófono roto => Çilófono roto
    if text[0] == "X": text = VAF_UP + text[1:]
    if text[0] == "x": text = VAF + text[1:]

    # If the /ks/ sound is between vowels
    # Axila => Aççila | Éxito => Éççito
    text = re.sub(ur'(a|e|i|o|u|á|é|í|ó|ú|Á|É|Í|Ó|Ú)(x)(a|e|i|o|u|á|é|í|ó|ú|Á|É|Í|Ó|Ú)', replace_intervowel_with_case, text, flags=re.IGNORECASE)

    # Every word starting with /ks/
    text = re.sub(ur'\b(x)', replace_with_case, text, flags=re.IGNORECASE|re.UNICODE)

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

    text = re.sub(ur'(l)(b|c|ç|Ç|g|s|d|f|g|h|k|m|p|q|r|t|x|z)', replace_with_case, text, flags=re.IGNORECASE)
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

    text = re.sub(ur'(z|s)(a|e|i|o|u|á|é|í|ó|ú|Á|É|Í|Ó|Ú|â|ê|î|ô|û|Â|Ê|Î|Ô|Û)', replace_with_case, text, flags=re.IGNORECASE)
    text = re.sub(ur'(c)(e|i|é|í|É|Í|â|ê|î|ô|û|Â|Ê|Î|Ô|Û)', replace_with_case, text, flags=re.IGNORECASE)

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
    text = re.sub(ur'(a|e|i|o|u|á|é|í|ó|ú|Á|É|Í|Ó|Ú)(l|r)(s)(t)', replace_lstrst_with_case, text, flags=re.IGNORECASE)
    # aerotransporte => aerotrâpporte | translado => trâl-lado | transcendente => trâççendente | postoperatorio => pôttoperatorio | postpalatal => pôppalatal
    text = re.sub(ur'(tr|p)(a|o)(ns|st)(b|c|ç|Ç|d|f|g|h|j|k|l|m|n|p|q|s|t|v|w|x|y|z)', replace_transpost_with_case, text, flags=re.IGNORECASE|re.UNICODE)
    # abstracto => âttrâtto | adscrito => âccrito | perspectiva => pêrppêttiba
    text = re.sub(ur'(a|e|i|o|u|á|é|í|ó|ú|Á|É|Í|Ó|Ú)(b|d|n|r)(s)(b|c|ç|Ç|d|f|g|h|j|k|l|m|n|p|q|s|t|v|w|x|y|z)', replace_bdnr_s_with_case, text, flags=re.IGNORECASE|re.UNICODE)
    # atlántico => âl-lántico | orla => ôl-la | adlátere => âl-látere | tesla => têl-la ...
    text = re.sub(ur'(a|e|i|o|u|á|é|í|ó|ú|Á|É|Í|Ó|Ú)(d|j|r|s|t|x|z)(l)', replace_l_with_case, text, flags=re.IGNORECASE|re.UNICODE)

    # General digraph rules.
    text = re.sub(ur'(a|e|i|o|u|á|é|í|ó|ú|Á|É|Í|Ó|Ú)(' + u'|'.join(DIGRAPHS) + ')', replace_digraph_with_case, text, flags=re.IGNORECASE|re.UNICODE)

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

        prefix = match.group(1)
        suffix_vowel = match.group(2)
        suffix_const = match.group(3)

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

        if suffix_vowel in (u'á',u'é',u'í',u'ó',u'ú',u'Á',u'É',u'Í',u'Ó',u'Ú'):
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

        prefix = match.group(1)
        suffix_vowel = match.group(2)
        suffix_const = match.group(3)

        if any(s in prefix for s in (u'á',u'é',u'í',u'ó',u'ú',u'Á',u'É',u'Í',u'Ó',u'Ú')):
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
            # Leave as it is. There shouldn't be any word with -eps ending withough accent.z
            return prefix + suffix_vowel + suffix_const

    def replace_intervowel_d_end_with_case(match):

        exceptions = [
            "fado", "cado", "nado", "priado",
            "fabada", "fada", "ada", "hada", "lada", "rada",
            "aikido", "buxido", "xido", "cuido", "cupido", "descuido", "despido", "ehido", "embido", "fido", "gido", "ido", "infido", "laido", "libido", "nido", "nucleido", "sonido", "suido"
        ]

        prefix = match.group(1)
        suffix_vowel_a = match.group(2)
        suffix_d_char = match.group(3)
        suffix_vowel_b = match.group(4)

        suffix = suffix_vowel_a + suffix_d_char + suffix_vowel_b
        word = prefix + suffix

        if word.lower() in exceptions:
            return word
        elif not any(s in prefix for s in (u'á',u'é',u'í',u'ó',u'ú',u'Á',u'É',u'Í',u'Ó',u'Ú')):
            # Ending word -ada rules
            if suffix.lower() == u'ada':
                if suffix_vowel_b.isupper():
                    return prefix + u'Á'
                else:
                    return prefix + u'á'
            # Ending word -ado rules
            elif suffix.lower() == u'ado':
                return prefix + suffix_vowel_a + suffix_vowel_b
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

    text = re.sub(ur'\b(\w+?)(e)(ps)\b', replace_eps_end_with_case, text, flags=re.IGNORECASE|re.UNICODE)
    text = re.sub(ur'\b(\w+?)(a|e|i|o|u|á|é|í|ó|ú|Á|É|Í|Ó|Ú)(d)\b', replace_d_end_with_case, text, flags=re.IGNORECASE|re.UNICODE)
    text = re.sub(ur'\b(\w+?)(a|e|i|o|u|á|é|í|ó|ú|Á|É|Í|Ó|Ú)(s)\b', replace_s_end_with_case, text, flags=re.IGNORECASE|re.UNICODE)
    text = re.sub(ur'\b(\w+?)(a|e|i|o|u|á|é|í|ó|ú|Á|É|Í|Ó|Ú)(b|f|g|j|l|p|r|t|x|z)\b', replace_const_end_with_case, text, flags=re.IGNORECASE|re.UNICODE)

    # Intervowel /d/ replacements
    text = re.sub(ur'\b(\w+?)(a|i|í|Í)(d)(o|a)\b', replace_intervowel_d_end_with_case, text, flags=re.IGNORECASE|re.UNICODE)

    return text

# Main function
def cas_to_epa(text, debug=False):
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
        digraph_rules
    ]

    text = unicode(text, 'utf-8')

    for rule in rules:
        text = rule(text)
        if debug: print rule.func_name + ' => ' + text

    return text

class EPAError(Exception):
    def __init__(self, message, errors):

        # Call the base class constructor with the parameters it needs
        super(EPAError, self).__init__(message)

        # Now for your custom code...
        self.errors = errors