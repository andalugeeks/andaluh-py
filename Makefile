.PHONY: sync install build publish clean help test lint check tox-run check-uv run demo

check-uv:
	@if ! command -v uv &> /dev/null; then \
		echo "uv no está instalado. Instálalo con: curl -LsSf https://astral.sh/uv/install.sh | sh"; \
		exit 1; \
	fi

help: ## Muestra esta ayuda
	@echo "Ayuda: make <target>"
	@echo "Targets disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

sync: check-uv ## Sincroniza dependencias y crea entorno virtual con uv
	@echo "Sincronizando dependencias con uv..."
	@uv sync --extra dev
	@echo "Entorno sincronizado"

install: check-uv sync ## Instala el módulo andaluh en modo desarrollo
	@echo "Instalando módulo andaluh..."
	@uv pip install -e .
	@echo "Módulo andaluh instalado en modo desarrollo"

build: check-uv ## Construye el paquete
	@echo "Construyendo paquete..."
	@if [ -d "dist" ]; then \
		echo "ADVERTENCIA: Limpia el directorio dist primero."; \
		exit 1; \
	fi
	@uv build
	@echo "Paquete construido"

publish: check-uv build ## Publica el paquete
	@echo "Publicando paquete..."
	@uv publish
	@echo "Paquete publicado"

clean: check-uv ## Limpia archivos generados
	@echo "Limpiando..."
	@rm -rf dist build *.egg-info
	@rm -rf .tox
	@find . -type d -name __pycache__ -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@echo "Limpieza completada"

test: check-uv sync ## Ejecuta los tests
	@echo "Ejecutando tests..."
	@uv run pytest --cov=andaluh tests/
	@echo "Tests completados"

lint: check-uv sync ## Ejecuta linting con flake8
	@echo "Ejecutando linting..."
	@uv run flake8 andaluh/ bin/
	@echo "Linting completado"

tox-run: check-uv sync ## Ejecuta tox
	@echo "Ejecutando tox..."
	@uv run tox
	@echo "Tox completado"

check: test lint ## Ejecuta tests y linting
	@echo "Verificación completa"

run: check-uv sync ## Ejecuta el CLI andaluh (uso: make run TEXT="tu texto aquí")
	@echo "Ejecutando andaluh CLI..."
	@if [ -z "$(TEXT)" ]; then \
		uv run python bin/andaluh --help; \
	else \
		uv run python bin/andaluh "$(TEXT)" $(ARGS); \
	fi

demo: check-uv sync ## Ejecuta una demostración del CLI andaluh
	@echo "Demostración de andaluh:"
	@echo "Texto original: 'Hola, ¿cómo estás? ¡Qué tal el día!'"
	@echo "Transliteración:"
	@uv run python bin/andaluh "Hola, ¿cómo estás? ¡Qué tal el día!"
