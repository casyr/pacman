help:
	@echo "Available commands:"
	@echo "  make install                  - Install project dependencies"
	@echo "  make run                      - Execute the main script"
	@echo "  make debug                    - Run the main script in debug mode (pdb)"
	@echo "  make lint                     - Run flake8 and mypy with standard checks"
	@echo "  make package                  - Execute script building package"
	@echo "  make clean                    - Remove all temporary files and caches"

install:
	uv sync

run: install
	uv run python3 pac-man.py config.json

debug: install
	uv run python3 -m pdb pac-man.py config.json

lint: 
	uv run flake8 src/ && uv run mypy src/ --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

package:
	./package.sh

clean:
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name "logs" -exec rm -rf {} +
	@rm -rf .venv
	@rm -rf data
	@rm -rf pacman_release.zip

.PHONY:
	help install run debug lint package clean