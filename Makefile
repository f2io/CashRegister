PHONY: test lint format typecheck qa

test:
	@echo "Running tests..."
	python -m pytest tests

lint:
	@echo "Running linters..."
	ruff check --fix .

format:
	@echo "Running code formatter..."
	ruff format .

typecheck:
	@echo "Running type checks..."
	ty check

qa: format lint typecheck
	@echo "All quality checks passed!"
