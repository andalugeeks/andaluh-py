## v0.4.1 (2025-07-06)

### Fix

- forces pipelines execution

## v0.4.0 (2025-07-06)

### Feat

- **Makefile**: adds tox-run target
- Added support to python 3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 3.12
- Adds support for python3.11

### Fix

- **pyproject.toml**: adds commitizen configuration (#22)
- **bin/andaluh**: replace python shebang by python3
- fixes -e py to tox execution in pythonapp.yml
- fixes envlist in tox.ini
- fixes issue in pythonap.yml versions
- Keep only python 3.8, 3.9, 3.10, 3.11 and 3.12

### Refactor

- Preparing package for 1.0.0 release
