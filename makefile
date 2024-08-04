# o erro makefile:17: *** missing separator. Stop.,
# ocorre porque  deve ser feita usando o (TAB) e não com espaços.


VENV := .venv

	PYTHON := $(VENV)/bin/python
	PIP := $(VENV)/bin/pip

ifeq ($(OS),Windows_NT)
	PYTHON := $(VENV)\Scripts\python.exe
	PIP := $(VENV)\Scripts\pip.exe
else
	PYTHON := $(VENV)/bin/python
	PIP := $(VENV)/bin/pip
endif

all: install run

$(VENV):
	python -m venv $(VENV)

install: $(VENV)
	$(PIP) install -r requirements.txt

run: install
	$(PYTHON) -m uvicorn main:app --reload