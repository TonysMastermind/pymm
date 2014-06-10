PYTHON ?= python2.7

all: build test doc

build:
	$(PYTHON) ./setup.py build

doc:
	$(PYTHON) ./setup.py build_sphinx

runtest:
	PYTHONPATH=$(PWD)/lib:$(PYTHONPATH) $(PYTHON) $(TESTS)

test: build
	$(PYTHON) ./setup.py nosetests

clean:
	$(PYTHON) ./setup.py clean

.PHONY: build test doc
