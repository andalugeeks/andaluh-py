#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: ts=4
###
# 
# Copyright (c) 2018-2019 Andalugeeks
# Authors:
# - Ksar Feui <a.moreno.losana@gmail.com>
# - J. Félix Ontañón <felixonta@gmail.com>

# Useful for calculate the circumflex equivalents.
VOWELS_ALL_NOTILDE = u'aeiouâêîôûAEIOUÂÊÎÔÛ'
VOWELS_ALL_TILDE = u'áéíóúâêîôûÁÉÍÓÚÂÊÎÔÛ'

# EPA character for Voiceless alveolar fricative /s/ https://en.wikipedia.org/wiki/Voiceless_alveolar_fricative
VAF = u'ç'

# EPA character for Voiceless velar fricative /x/ https://en.wikipedia.org/wiki/Voiceless_velar_fricative
VVF = u'h'

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

H_RULES_EXCEPT = {
    u'haz': u'âh', u'hez': u'êh', u'hoz': u'ôh',
    u'oh': u'ôh',
    u'yihad': u'yihá',
    u'h': u'h' # Keep an isolated h as-is
}

GJ_RULES_EXCEPT = {
    u'gin': u'yin', u'jazz': u'yâh', u'jet': u'yêh'
}

V_RULES_EXCEPT = {
    u'vis': u'bî', u'ves': u'bêh'
}

LL_RULES_EXCEPT = {
    u'grill': u'grîh'
}

WORDEND_D_RULES_EXCEPT = {
    u'çed': u'çêh'
}

WORDEND_S_RULES_EXCEPT = {
    u'bies': u'biêh', u'bis': u'bîh', u'blues': u'blû', u'bus': u'bûh',
    u'dios': u'diôh', u'dos': u'dôh',
    u'gas': u'gâh', u'gres': u'grêh', u'gris': u'grîh',
    u'luis': u'luîh',
    u'mies': u'miêh', u'mus': u'mûh',
    u'os': u'ô',
    u'pis': u'pîh', u'plus': u'plûh', u'pus': u'pûh',
    u'ras': u'râh', u'res': u'rêh',
    u'tos': u'tôh', u'tres': u'trêh', u'tris': u'trîh'
}

WORDEND_CONST_RULES_EXCEPT = {
    u'al': u'al', u'cual': u'cuâ', u'del': u'del', u'dél': u'dél', u'el':'el', u'él':'èl', u'tal': u'tal', u'bil': u'bîl',
    # TODO: uir = huir. Maybe better to add the exceptions on h_rules?
    u'por': u'por', u'uir': u'huîh',
    # sic, tac
    u'çic': u'çic', u'tac': u'tac',
    u'yak': u'yak',
    u'stop': u'êttôh', u'bip': u'bip'
}

WORDEND_D_INTERVOWEL_RULES_EXCEPT = {
    # Ending with -ado
    u"fado": u"fado", u"cado": u"cado", u"nado": u"nado", u"priado": u"priado",
    # Ending with -ada
    u"fabada": u"fabada", u'fabadas':u'fabadas', u"fada": u"fada", u"ada": u"ada", u"lada": u"lada", u"rada": u"rada",
    # Ending with -adas
    u"adas": u"adas", u"radas": u"radas", u"nadas": u"nadas",
    # Ending with -ido
    u"aikido": u"aikido", u"bûççido": u"bûççido", u"çido": u"çido", u"cuido": u"cuido", u"cupido": u"cupido", u"descuido": u"descuido",
    u"despido": u"despido", u"eido": u"eido", u"embido": u"embido", u"fido": u"fido", u"hido": u"hido", u"ido": u"ido", u"infido": u"infido",
    u"laido": u"laido", u"libido": u"libido", u"nido": u"nido", u"nucleido": u"nucleido", u"çonido": u"çonido", u"çuido": u"çuido"
}

ENDING_RULES_EXCEPTION = {
    # Exceptions to digraph rules with nm
    u'biêmmandao':u'bienmandao', u'biêmmeçabe':u'bienmeçabe', u'buêmmoço':u'buenmoço', u'çiêmmiléçima':u'çienmiléçima', u'çiêmmiléçimo':u'çienmiléçimo', u'çiêmmilímetro':u'çienmilímetro', u'çiêmmiyonéçima':u'çienmiyonéçima', u'çiêmmiyonéçimo':u'çienmiyonéçimo', u'çiêmmirmiyonéçima':u'çienmirmiyonéçima', u'çiêmmirmiyonéçimo':u'çienmirmiyonéçimo',
    # Exceptions to l rules
    u'marrotadôh':u'mârrotadôh', u'marrotâh':u'mârrotâh', u'mirrayâ':u'mîrrayâ',
    # Exceptions to psico pseudo rules
    u'herôççiquiatría':u'heroçiquiatría', u'herôççiquiátrico':u'heroçiquiátrico', u'farmacôççiquiatría':u'farmacoçiquiatría', u'metempçícoçî':u'metemçícoçî', u'necróçico':u'necróççico', u'pampçiquîmmo':u'pamçiquîmmo',
    # Other exceptions
    u'antîççerôttármico':u'antiçerôttármico', u'eclampçia':u'eclampçia', u'pôttoperatorio':u'pôççoperatorio', u'çáccrito':u'çánccrito', u'manbîh':u'mambîh', u'cômmelináçeo':u'commelináçeo', u'dîmmneçia':u'dînneçia', u'todo': u'tó', u'todô': u'tôh', u'toda': u'toa', u'todâ': u'toâ',
    # Other exceptions monosyllables
    u'as':u'âh', u'clown':u'claun', u'crack':u'crâh', u'down':u'daun', u'es':u'êh', u'ex':u'êh', u'ir':u'îh', u'miss':u'mîh', u'muy':u'mu', u'ôff':u'off', u'os':u'ô', u'para':u'pa', u'ring':u'rin', u'rock':u'rôh', u'spray':u'êppray', u'sprint':u'êpprín', u'wau':u'guau'
}