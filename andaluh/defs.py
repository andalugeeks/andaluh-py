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

# Useful for calculate the circumflex equivalents.
VOWELS_ALL_NOTILDE = 'aeiouâêîôûAEIOUÂÊÎÔÛ'
VOWELS_ALL_TILDE = 'áéíóúâêîôûÁÉÍÓÚÂÊÎÔÛ'

# EPA character for Voiceless alveolar fricative /s/
# https://en.wikipedia.org/wiki/Voiceless_alveolar_fricative
VAF = 'ç'

# EPA character for Voiceless velar fricative /x/
# https://en.wikipedia.org/wiki/Voiceless_velar_fricative
VVF = 'h'

# Digraphs producers. (vowel)(const)(const) that triggers the general
# digraph rule
DIGRAPHS = [
    "bb",
    "bc",
    "bç",
    "bÇ",
    "bd",
    "bf",
    "bg",
    "bh",
    "bm",
    "bn",
    "bp",
    "bq",
    "bt",
    "bx",
    "by",
    "cb",
    "cc",
    "cç",
    "cÇ",
    "cd",
    "cf",
    "cg",
    "ch",
    "cm",
    "cn",
    "cp",
    "cq",
    "ct",
    "cx",
    "cy",
    "db",
    "dc",
    "dç",
    "dÇ",
    "dd",
    "df",
    "dg",
    "dh",
    "dl",
    "dm",
    "dn",
    "dp",
    "dq",
    "dt",
    "dx",
    "dy",
    "fb",
    "fc",
    "fç",
    "fÇ",
    "fd",
    "ff",
    "fg",
    "fh",
    "fm",
    "fn",
    "fp",
    "fq",
    "ft",
    "fx",
    "fy",
    "gb",
    "gc",
    "gç",
    "gÇ",
    "gd",
    "gf",
    "gg",
    "gh",
    "gm",
    "gn",
    "gp",
    "gq",
    "gt",
    "gx",
    "gy",
    "jb",
    "jc",
    "jç",
    "jÇ",
    "jd",
    "jf",
    "jg",
    "jh",
    "jl",
    "jm",
    "jn",
    "jp",
    "jq",
    "jr",
    "jt",
    "jx",
    "jy",
    "lb",
    "lc",
    "lç",
    "lÇ",
    "ld",
    "lf",
    "lg",
    "lh",
    "ll",
    "lm",
    "ln",
    "lp",
    "lq",
    "lr",
    "lt",
    "lx",
    "ly",
    "mm",
    'mn',
    'nm',
    'nn',
    "pb",
    "pc",
    "pç",
    "pÇ",
    "pd",
    "pf",
    "pg",
    "ph",
    "pm",
    "pn",
    "pp",
    "pq",
    "pt",
    "px",
    "py",
    "rn",
    "sb",
    "sc",
    "sç",
    "sÇ",
    "sd",
    "sf",
    "sg",
    "sh",
    "sk",
    "sl",
    "sm",
    "sn",
    "sñ",
    "sp",
    "sq",
    "sr",
    "st",
    "sx",
    "sy",
    "tb",
    "tc",
    "tç",
    "tÇ",
    "td",
    "tf",
    "tg",
    "th",
    "tl",
    "tm",
    "tn",
    "tp",
    "tq",
    "tt",
    "tx",
    "ty",
    "xb",
    "xc",
    "xç",
    "xÇ",
    "xd",
    "xf",
    "xg",
    "xh",
    "xl",
    "xm",
    "xn",
    "xp",
    "xq",
    "xr",
    "xt",
    "xx",
    "xy",
    "zb",
    "zc",
    "zç",
    "zÇ",
    "zd",
    "zf",
    "zg",
    "zh",
    "zl",
    "zm",
    "zn",
    "zp",
    "zq",
    "zr",
    "zt",
    "zx",
    "zy"]

H_RULES_EXCEPT = {
    'haz': 'âh',
    'hez': 'êh',
    'hoz': 'ôh',
    'oh': 'ôh',
    'yihad': 'yihá',
    'h': 'h'  # Keep an isolated h as-is
}

GJ_RULES_EXCEPT = {
    'gin': 'yin',
    'jazz': 'yâh',
    'jet': 'yêh'
}

V_RULES_EXCEPT = {
    'vis': 'bî',
    'ves': 'bêh'
}

LL_RULES_EXCEPT = {
    'grill': 'grîh'
}

WORDEND_D_RULES_EXCEPT = {
    'çed': 'çêh'
}

WORDEND_S_RULES_EXCEPT = {
    'bies': 'biêh', 'bis': 'bîh', 'blues': 'blû', 'bus': 'bûh',
    'dios': 'diôh', 'dos': 'dôh',
    'gas': 'gâh', 'gres': 'grêh', 'gris': 'grîh',
    'luis': 'luîh',
    'mies': 'miêh', 'mus': 'mûh',
    'os': 'ô',
    'pis': 'pîh', 'plus': 'plûh', 'pus': 'pûh',
    'ras': 'râh', 'res': 'rêh',
    'tos': 'tôh', 'tres': 'trêh', 'tris': 'trîh'
}

WORDEND_CONST_RULES_EXCEPT = {
    'al': 'al',
    'cual': 'cuâ',
    'del': 'del',
    'dél': 'dél',
    'el': 'el',
    'él': 'èl',
    'tal': 'tal',
    'bil': 'bîl',
    # TODO: uir = huir. Maybe better to add the exceptions on h_rules?
    'por': 'por', 'uir': 'huîh',
    # sic, tac
    'çic': 'çic', 'tac': 'tac',
    'yak': 'yak',
    'stop': 'êttôh',
    'bip': 'bip'
}

WORDEND_D_INTERVOWEL_RULES_EXCEPT = {
    # Ending with -ado
    "fado": "fado", "cado": "cado", "nado": "nado", "priado": "priado",
    # Ending with -ada
    "fabada": "fabada",
    'fabadas': 'fabadas',
    "fada": "fada",
    "ada": "ada",
    "lada": "lada",
    "rada": "rada",
    # Ending with -adas
    "adas": "adas", "radas": "radas", "nadas": "nadas",
    # Ending with -ido
    "aikido": "aikido",
    "bûççido": "bûççido",
    "çido": "çido",
    "cuido": "cuido",
    "cupido": "cupido",
    "descuido": "descuido",
    "despido": "despido",
    "eido": "eido",
    "embido": "embido",
    "fido": "fido",
    "hido": "hido",
    "ido": "ido",
    "infido": "infido",
    "laido": "laido",
    "libido": "libido",
    "nido": "nido",
    "nucleido": "nucleido",
    "çonido": "çonido",
    "çuido": "çuido"
}

ENDING_RULES_EXCEPTION = {
    # Exceptions to digraph rules with nm
    'biêmmandao': 'bienmandao',
    'biêmmeçabe': 'bienmeçabe',
    'buêmmoço': 'buenmoço',
    'çiêmmiléçima': 'çienmiléçima',
    'çiêmmiléçimo': 'çienmiléçimo',
    'çiêmmilímetro': 'çienmilímetro',
    'çiêmmiyonéçima': 'çienmiyonéçima',
    'çiêmmiyonéçimo': 'çienmiyonéçimo',
    'çiêmmirmiyonéçima': 'çienmirmiyonéçima',
    'çiêmmirmiyonéçimo': 'çienmirmiyonéçimo',
    # Exceptions to l rules
    'marrotadôh': 'mârrotadôh',
    'marrotâh': 'mârrotâh',
    'mirrayâ': 'mîrrayâ',
    # Exceptions to psico pseudo rules
    'herôççiquiatría': 'heroçiquiatría',
    'herôççiquiátrico': 'heroçiquiátrico',
    'farmacôççiquiatría': 'farmacoçiquiatría',
    'metempçícoçî': 'metemçícoçî',
    'necróçico': 'necróççico',
    'pampçiquîmmo': 'pamçiquîmmo',
    # Other exceptions
    'antîççerôttármico': 'antiçerôttármico',
    'eclampçia': 'eclampçia',
    'pôttoperatorio': 'pôççoperatorio',
    'çáccrito': 'çánccrito',
    'manbîh': 'mambîh',
    'cômmelináçeo': 'commelináçeo',
    'dîmmneçia': 'dînneçia',
    'todo': 'tó',
    'todô': 'tôh',
    'toda': 'toa',
    'todâ': 'toâ',
    # Other exceptions monosyllables
    'as': 'âh',
    'clown': 'claun',
    'crack': 'crâh',
    'down': 'daun',
    'es': 'êh',
    'ex': 'êh',
    'ir': 'îh',
    'miss': 'mîh',
    'muy': 'mu',
    'ôff': 'off',
    'os': 'ô',
    'para': 'pa',
    'ring': 'rin',
    'rock': 'rôh',
    'spray': 'êppray',
    'sprint': 'êpprín',
    'wau': 'guau'
}
