.PHONY: sync install build publish clean help test lint check tox-run check-uv run demo update-dev-requirements check-dev-requirements

check-uv:
	@if ! command -v uv &> /dev/null; then \
		echo "❌ uv no está instalado."; \
		echo "📥 Instálalo con: curl -LsSf https://astral.sh/uv/install.sh | sh"; \
		echo "📖 Más info: https://docs.astral.sh/uv/"; \
		exit 1; \
	fi

help: ## Muestra esta ayuda
	@echo "Ayuda: make <target>"
	@echo "Targets disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

sync: check-uv ## Sincroniza dependencias y crea entorno virtual con uv
	@echo "🔄 Sincronizando dependencias con uv..."
	@uv sync --extra dev
	@echo "📝 Actualizando dev-requirements.txt..."
	@$(MAKE) update-dev-requirements --no-print-directory
	@echo "✅ Entorno sincronizado"

install: check-uv sync ## Instala el módulo andaluh en modo desarrollo
	@echo "⚙️  Instalando módulo andaluh en modo desarrollo..."
	@uv pip install -e .
	@echo "✅ Módulo andaluh instalado en modo desarrollo"

build: check-uv ## Construye el paquete
	@echo "Construyendo paquete..."
	@if [ -d "dist" ]; then \
		echo "🧹 Limpiando directorio dist existente..."; \
		rm -rf dist; \
	fi
	@uv build
	@echo "✅ Paquete construido exitosamente en dist/"

publish: check-uv build ## Publica el paquete
	@echo "📦 Publicando paquete a PyPI..."
	@uv publish
	@echo "✅ Paquete publicado exitosamente"

clean: check-uv ## Limpia archivos generados
	@echo "🧹 Limpiando archivos generados..."
	@rm -rf dist build *.egg-info
	@rm -rf .tox
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Limpieza completada"

test: check-uv sync ## Ejecuta los tests
	@echo "🧪 Ejecutando tests..."
	@uv run pytest --cov=andaluh tests/
	@echo "✅ Tests completados"

lint: check-uv sync ## Ejecuta linting con flake8
	@echo "🔍 Ejecutando linting..."
	@uv run flake8 andaluh/ bin/
	@echo "✅ Linting completado"

tox-run: check-uv sync ## Ejecuta tox para pruebas en entornos aislados o múltiples versiones de Python
	@echo "🐍 Ejecutando tox (tests en múltiples versiones de Python)..."
	@uv run tox
	@echo "✅ Tox completado"

check: test lint check-dev-requirements ## Ejecuta tests, linting y verificaciones
	@echo "✅ Verificación completa"

run: check-uv sync ## Ejecuta el CLI andaluh (uso: make run TEXT="tu texto aquí")
	@echo "🚀 Ejecutando andaluh CLI..."
	@if [ -z "$(TEXT)" ]; then \
		uv run python bin/andaluh --help; \
	else \
		uv run python bin/andaluh "$(TEXT)" $(ARGS); \
	fi

demo: check-uv sync ## Ejecuta una demostración del CLI andaluh
	@echo "🎯 Demostración de andaluh:"
	@echo "Texto original: 'Hola, ¿cómo estás? ¡Qué tal el día!'"
	@echo "Transliteración:"
	@uv run python bin/andaluh "Hola, ¿cómo estás? ¡Qué tal el día!"

update-dev-requirements: check-uv ## Actualiza dev-requirements.txt desde pyproject.toml
	@echo "📝 Actualizando dev-requirements.txt desde pyproject.toml..."
	@uv export --extra dev --format requirements-txt --no-hashes > dev-requirements.txt.tmp
	@grep -v "^-e" dev-requirements.txt.tmp > dev-requirements.txt || true
	@rm -f dev-requirements.txt.tmp
	@echo "✅ dev-requirements.txt actualizado"

check-dev-requirements: check-uv ## Verifica si dev-requirements.txt está sincronizado
	@echo "🔍 Verificando sincronización de dev-requirements.txt..."
	@uv export --extra dev --format requirements-txt --no-hashes > dev-requirements.txt.tmp
	@grep -v "^-e" dev-requirements.txt.tmp > dev-requirements.txt.expected || true
	@rm -f dev-requirements.txt.tmp
	@if ! cmp -s dev-requirements.txt dev-requirements.txt.expected 2>/dev/null; then \
		echo "⚠️  dev-requirements.txt no está sincronizado con pyproject.toml"; \
		echo "💡 Ejecuta 'make update-dev-requirements' para sincronizar"; \
		rm -f dev-requirements.txt.expected; \
		exit 1; \
	else \
		echo "✅ dev-requirements.txt está sincronizado"; \
		rm -f dev-requirements.txt.expected; \
	fi
