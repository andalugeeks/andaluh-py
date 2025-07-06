# Andaluh-py

Transliterate español (spanish) spelling to andaluz proposals

## Table of Contents

- [Description](#description)
- [Requirements](#requirements)
- [Usage](#usage)
  - [Command line tool](#command-line-tool)
  - [Development usage](#development-usage)
  - [Python library](#python-library)
- [Installation](#installation)
  - [From PyPI repository](#from-pypi-repository)
  - [From source code](#from-source-code)
- [Roadmap](#roadmap)
- [Support](#support)
- [Contributing](#contributing)

## Description

The **Andalusian varieties of [Spanish]** (Spanish: *andalûh*; Andalusian) are spoken in Andalusia, Ceuta, Melilla, and Gibraltar. They include perhaps the most distinct of the southern variants of peninsular Spanish, differing in many respects from northern varieties, and also from Standard Spanish. Further info: https://en.wikipedia.org/wiki/Andalusian_Spanish.

This package introduces transliteration functions to convert *español* (spanish) spelling to andaluz. As there's no official or standard andaluz spelling, andaluh-py is adopting the **EPA proposal (Er Prinzipito Andaluh)**. Further info: https://andaluhepa.wordpress.com. Other andaluz spelling proposals are planned to be added as well.

## Requirements

- Python 3.9 or higher
- For development: [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Usage

### Command line tool

Use EPA transliterator from the command line with the **andaluh** tool:

```bash
$ andaluh -h
usage: andaluh [-h] [-e {s,z,h}] [-j] [-i FILE] [text]

Transliterate español (spanish) spelling to Andalûh EPA.

positional arguments:
  text        Text to transliterate. Enclosed in quotes for multiple words.

optional arguments:
  -h, --help  show this help message and exit
  -e {s,z,h}  Enforce seseo, zezeo or heheo instead of cedilla (standard).
  -j          Keep /x/ sounds as J instead of /h/
  -i FILE     Transliterates the plain text input file to stdout

$ andaluh "El veloz murciélago hindú comía feliz cardillo y kiwi. La cigüeña tocaba el saxofón detrás del palenque de paja."
Er belôh murçiélago indú comía felîh cardiyo y kiwi. La çigueña tocaba er çâççofón detrâh der palenque de paha.

$ andaluh -e z -j "El veloz murciélago hindú comía feliz cardillo y kiwi. La cigüeña tocaba el saxofón detrás del palenque de paja."
Er belôh murziélago indú comía felîh cardiyo y kiwi. La zigueña tocaba er zâzzofón detrâh der palenque de paja.
```

You also can transliterate files using the `-i` option:

```bash
$ andaluh -i input.txt > output.txt
```

### EPA Syllabifier

The package includes a **syllabify** tool for syllabifying words using EPA rules:

```bash
$ syllabify -h
usage: syllabify [-h] [--word WORD] [--file FILE]

Syllabify a word

optional arguments:
  -h, --help            show this help message and exit
  --word WORD, -w WORD  The EPA word to syllabify
  --file FILE, -f FILE  The file to syllabify

# Syllabify a single word
$ syllabify --word "murciélago"
mur-cié-la-go

$ syllabify -w "andaluz"
an-da-luz

# Syllabify an entire file
$ syllabify --file input.txt
```

### Development usage

If you're working with the source code, you can use the convenient make commands:

```bash
# Quick demo
$ make demo
Demostración de andaluh:
Texto original: 'Hola, ¿cómo estás? ¡Qué tal el día!'
Transliteración:
Ola, ¿cómo êttâh? ¡Qué tal er día!

# Custom text
$ make run TEXT="Buenos días desde Andalucía"
Guenô díâ dêdde Andaluçía

# With options (seseo + keep 'j' sounds)
$ make run TEXT="Buenas tardes tengan ustedes" ARGS="-e h -j"
Guenâ tardê tengan ûttedê
```

### Python library

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

### From PyPI repository

```bash
# Using pip
$ pip install andaluh

# Using uv (recommended)
$ uv add andaluh
```

### From source code

#### Development setup with uv (recommended)

```bash
# Clone the repository
$ git clone https://github.com/andalugeeks/andaluh-py.git
$ cd andaluh-py

# Setup development environment with uv
$ uv sync --extra dev

# Run tests
$ uv run pytest

# Or use the Makefile
$ make sync    # Setup environment
$ make test    # Run tests
$ make demo    # Try the CLI
```

#### Traditional setup with pip

```bash
# Install in development mode
~/andaluh-py$ pip install -e .
```

### Development commands

This project uses modern Python tooling with `uv` and `pyproject.toml`. Available make commands:

```bash
make sync          # Setup development environment
make test          # Run tests with coverage
make lint          # Run code linting
make check         # Run tests + linting
make demo          # Try the CLI with example text
make run TEXT="..."# Run CLI with custom text
make build         # Build the package
make clean         # Clean generated files
```

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

### Development Setup

This project uses modern Python tooling:
- **[uv](https://docs.astral.sh/uv/)** for fast dependency management
- **pyproject.toml** for project configuration (PEP 621)
- **pytest** for testing with coverage
- **flake8** for code linting
- **tox** for testing across Python versions

Quick start for contributors:

```bash
# Clone and setup
git clone https://github.com/andalugeeks/andaluh-py.git
cd andaluh-py

# Setup development environment
make sync

# Run tests and linting
make check

# Try the CLI
make demo
```
