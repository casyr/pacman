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
	uv run python3 -m src.main $(MAP)

debug: install 
	uv run python3 -m pdb -m src.main

lint: 
	uv run flake8 . && uv run mypy src --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
clean:
	rm -rf .mypy_cache .venv .vscode __pycache__ src/__pycache__ .install src/parser/__pycache__ src/pathfinding/__pycache__ src/visualization/__pycache__ src/parser/state/__pycache__
	rm -rf logs/
.PHONY:
	install run debug lint clean