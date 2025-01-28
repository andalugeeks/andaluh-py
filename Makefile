
setup-build-tools:
	@echo "Setting up build tools..."
	@. .venv/bin/activate && python -m pip install build twine

build:
	@echo "Building..."
	@if [ -d "dist" ]; then \
		echo "WARNING: Clean dist directory first."; \
		exit 1; \
	fi
	@python -m build

publish:
	@echo "Publishing..."
	@. .venv/bin/activate && twine upload dist/*

clean:
	@echo "Cleaning..."
	@rm -rf dist build *.egg-info