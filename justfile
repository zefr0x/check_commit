alias t := test

_default:
	@just --list

test:
	pytest -v

lint_all:
	pre-commit run --all-files

lock:
	uv lock

sync:
	uv sync --all-extras --active

clean:
	find . -name "__pycache__" -type d -exec rm -r {} +
	rm -r .pytest_cache
