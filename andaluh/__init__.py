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

from .lib import epa
from .de import transformar_preposicion_de
from .en import transformar_preposicion_en
from .pa import transformar_preposicion_pa
from .ya import transformar_adverbio_ya
from .pronombres import transformar_pronombres_atonos
from .articulos import (transformar_articulos,
                        transformar_articulo_el,
                        transformar_articulo_la, )
from .contractions import apply_contractions, aplicar_contracciones

__all__ = [
    'epa',
    'transformar_preposicion_de',
    'transformar_preposicion_en',
    'transformar_preposicion_pa',
    'transformar_adverbio_ya',
    'transformar_pronombres_atonos',
    'transformar_articulos',
    'transformar_articulo_el',
    'transformar_articulo_la',
    'apply_contractions',
    'aplicar_contracciones',
]
