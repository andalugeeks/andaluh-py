.PHONY: create-venv activate-venv install setup-build-tools build publish clean

VENV_PYTHON=.venv/bin/python3
PYTHON_TESTS=.venv/bin/pytest

help: ## Muestra esta ayuda
	@echo "Ayuda: make <target>"
	@echo "Targets disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

create-venv: ## Crea un entorno virtual
	@echo "Creando entorno virtual..."
	@$(VENV_PYTHON) -m venv .venv
	@echo "Entorno virtual creado en .venv"

install: create-venv setup-build-tools ## Instala el módulo andaluh en modo desarrollo
	@echo "Instalando módulo andaluh..."
	@$(VENV_PYTHON) -m pip install -e .
	@echo "Módulo andaluh instalado en modo desarrollo"

setup-build-tools: ## Configura las herramientas de construcción
	@echo "Setting up build tools..."
	@$(VENV_PYTHON) -m pip install build twine

build: create-venv ## Construye el paquete
	@echo "Building..."
	@if [ -d "dist" ]; then \
		echo "WARNING: Clean dist directory first."; \
		exit 1; \
	fi
	@$(VENV_PYTHON) -m build

publish: create-venv ## Publica el paquete
	@echo "Publishing..."
	@twine upload dist/*

clean: create-venv ## Limpia el entorno
	@echo "Cleaning..."
	@rm -rf dist build *.egg-info

dev-dependencies: create-venv ## Instala las dependencias de desarrollo
	@echo "Installing development dependencies..."
	@$(VENV_PYTHON) -m pip install -r dev-requirements.txt
	@echo "Development dependencies installed"

run-tests: dev-dependencies ## Ejecuta los tests
	@echo "Running tests..."
	@$(PYTHON_TESTS)
