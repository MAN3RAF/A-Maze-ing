VENV = venv

PYTHON = $(VENV)/bin/python3

PIP = $(VENV)/bin/pip

NAME = a_maze_ing.py

CONFIG = config.txt


install:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install mypy
	$(PIP) install flake8
	$(PIP) install pytest


run:
	$(PYTHON) $(NAME) $(CONFIG)


debug:
	$(PYTHON) -m pdb $(NAME)


lint:
	$(PYTHON) -m flake8 *.py || true
	$(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs || true


lint-strict:
	$(PYTHON) -m flake8 *.py || true
	$(PYTHON) -m mypy . --strict || true


clean:
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf $(VENV)
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete


.PHONY:	install run debug clean lint lint-strict 