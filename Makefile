PYTHON ?= python2.7

all: build test doc

build:
	$(PYTHON) ./setup.py build

doc:
	$(PYTHON) ./setup.py build_sphinx

test: build
	$(PYTHON) ./setup.py nosetests $(NOSE_ARGS)

.PHONY: build test doc
