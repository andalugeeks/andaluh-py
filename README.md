# Andaluh-py

Transliterate español (spanish) spelling to andaluz proposals

## Table of Contents

- [Description](#description)
- [Usage](#usage)
- [Installation](#installation)
- [Roadmap](#roadmap)
- [Support](#support)
- [Contributing](#contributing)

## Description

The **Andalusian varieties of [Spanish]** (Spanish: *andaluz*; Andalusian) are spoken in Andalusia, Ceuta, Melilla, and Gibraltar. They include perhaps the most distinct of the southern variants of peninsular Spanish, differing in many respects from northern varieties, and also from Standard Spanish. Further info: https://en.wikipedia.org/wiki/Andalusian_Spanish.

This package introduces transliteration functions to convert *español* (spanish) spelling to andaluz. As there's no official or standard andaluz spelling, andaluh-py is adopting the **EPA proposal (Er Prinzipito Andaluh)**. Further info: https://andaluhepa.wordpress.com. Other andaluz spelling proposals are planned to be added as well.

## Usage

Use from the command line with the **andaluh** tool:

```
$ andaluh -h
usage: andaluh [-h] [-e {s,z,h}] [-j] text

Transliterate español (español) spelling to andaluz proposals

positional arguments:
  text        Text to transliterate. Enclose into quotes if there's more than
              one word

optional arguments:
  -h, --help  show this help message and exit
  -e {s,z,h}  Enforce seseo, zezeo or heheo instead of cedilla
  -j          Keep /x/ sounds as J instead of /h/

$ andaluh "El veloz murciélago hindú comía feliz cardillo y kiwi. La cigüeña tocaba el saxofón detrás del palenque de paja."
Er belôh murçiélago indú comía felîh cardiyo y kiwi. La çigueña tocaba er çâççofón detrâh der palenque de paha.

$ andaluh -e z -j "El veloz murciélago hindú comía feliz cardillo y kiwi. La cigüeña tocaba el saxofón detrás del palenque de paja."
Er belôh murziélago indú comía felîh cardiyo y kiwi. La zigueña tocaba er zâzzofón detrâh der palenque de paja.
```

Import the python library for your own projects:

```python
import andaluh

# Transliterate with andaluh EPA proposal
print(andaluh.epa("El veloz murciélago hindú comía feliz cardillo y kiwi. La cigüeña tocaba el saxofón detrás del palenque de paja."))
>>> Er belôh murçiélago indú comía felîh cardiyo y kiwi. La çigueña tocaba er çâççofón detrâh der palenque de paha.

# Enforce seseo instead of cedilla and 'j' for /x/ sounds. Show transliteration debug info.
print(andaluh.epa("El veloz murciélago hindú comía feliz cardillo y kiwi. La cigüeña tocaba el saxofón detrás palenque de paja.", vaf='s', vvf='j', debug=True))
h_rules => El veloz murciélago indú comía feliz cardillo y kiwi. La cigüeña tocaba el saxofón detrás palenque de paja.
x_rules => El veloz murciélago indú comía feliz cardillo y kiwi. La cigüeña tocaba el sâssofón detrás palenque de paja.
ch_rules => El veloz murciélago indú comía feliz cardillo y kiwi. La cigüeña tocaba el sâssofón detrás palenque de paja.
gj_rules => El veloz murciélago indú comía feliz cardillo y kiwi. La cigueña tocaba el sâssofón detrás palenque de paja.
v_rules => El beloz murciélago indú comía feliz cardillo y kiwi. La cigueña tocaba el sâssofón detrás palenque de paja.
ll_rules => El beloz murciélago indú comía feliz cardiyo y kiwi. La cigueña tocaba el sâssofón detrás palenque de paja.
l_rules => El beloz murciélago indú comía feliz cardiyo y kiwi. La cigueña tocaba el sâssofón detrás palenque de paja.
psico_pseudo_rules => El beloz murciélago indú comía feliz cardiyo y kiwi. La cigueña tocaba el sâssofón detrás palenque de paja.
vaf_rules => El beloz mursiélago indú comía feliz cardiyo y kiwi. La sigueña tocaba el sâssofón detrás palenque de paja.
word_ending_rules => El belôh mursiélago indú comía felîh cardiyo y kiwi. La sigueña tocaba el sâssofón detrâh palenque de paja.
digraph_rules => El belôh mursiélago indú comía felîh cardiyo y kiwi. La sigueña tocaba el sâssofón detrâh palenque de paja.
exception_rules => El belôh mursiélago indú comía felîh cardiyo y kiwi. La sigueña tocaba el sâssofón detrâh palenque de paja.
word_interaction_rules => Er belôh mursiélago indú comía felîh cardiyo y kiwi. La sigueña tocaba er sâssofón detrâh der palenque de paja.
Er belôh mursiélago indú comía felîh cardiyo y kiwi. La sigueña tocaba er sâssofón detrâh der palenque de paja.
```

## Installation

From PyPI repository

```
$ sudo pip install andaluh
```

From source code

```
~/andaluh-py$ pip install .
```
Remember use `-e` option for [develop mode](https://setuptools.readthedocs.io/en/latest/setuptools.html#development-mode).

## Roadmap

* Adding more andaluh spelling proposals.
* Contractions and inter-word interaction rules pending to be implemented.
* Silent /h/ sounds spelling rules pending to be implemented.
* Some spelling intervowel /d/ rules are still pending to be implemented.
* Transliteration rules for some consonant ending words still pending to be implemented.
* The andaluh EPA group is still deliberating about the 'k' letter.

## Support

Please [open an issue](https://github.com/andalugeeks/andaluh-py/issues/new) for support.

## Contributing

Please contribute using [Github Flow](https://guides.github.com/introduction/flow/). Create a branch, add commits, and open a pull request.
