VENV = .venv

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
	$(PYTHON) -m pip install --upgrade build


$(VENV):
	@if [ ! -d $(VENV) ]; then \
		make install; \
	fi


run: $(VENV)
	$(PYTHON) $(NAME) $(CONFIG)


debug: $(VENV)
	$(PYTHON) -m pdb $(NAME) $(CONFIG)


lint: $(VENV)
	$(PYTHON) -m flake8 . --exclude $(VENV)
	$(PYTHON) -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs


lint-strict: $(VENV)
	$(PYTHON) -m flake8 . --exclude $(VENV)
	$(PYTHON) -m mypy . --strict


clean:
	rm -rf .mypy_cache .pytest_cache
	rm -rf $(VENV)
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -maxdepth 1 -name "*.txt" ! -name "config.txt" -delete

build: $(VENV)
	$(PYTHON) -m build


.PHONY:	install run debug clean lint lint-strict