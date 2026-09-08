help:
	@echo "Available commands:"
	@echo "  make install                  - Install project dependencies"
	@echo "  make run                      - Execute the main script"
	@echo "  make debug                    - Run the main script in debug mode (pdb)"
	@echo "  make clean                    - Remove all temporary files and caches"
	@echo "  make lint                     - Run flake8 and mypy with standard checks"

install:
	uv sync

run: install
	uv run python3 -m src src/config.json

debug: install 
	uv run python3 -m pdb -m src src/config.json

lint: 
	uv run flake8 src/ && uv run mypy src/ --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

clean:
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name "logs" -exec rm -rf {} +
	@rm -rf .venv


.PHONY:
	help install run debug lint clean