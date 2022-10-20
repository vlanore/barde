all: examples/barde-0.1-py3-none-any.whl

examples/barde-0.1-py3-none-any.whl: dist/barde-0.1-py3-none-any.whl
	cp $< $@

dist/barde-0.1-py3-none-any.whl: $(wildcard barde/*.py)
	python3 -m build

.PHONY: clean
clean:
	rm -rf dist