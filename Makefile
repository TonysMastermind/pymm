all: build test doc

build:
	./setup.py build

doc:
	./setup.py build_sphinx

test: build
	./setup.py nosetests $(NOSE_ARGS)

.PHONY: build test doc
