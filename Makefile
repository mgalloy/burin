VERSION=`python setup.py --version`

.PHONY: clean dist doc check test unit

clean:
	echo "cleaning..."

doc:
	sphinx-apidoc -f --ext-autodoc -o docs/_api burin
	cd docs; make html

test:
	python setup.py test

unit:
	python setup.py test

dist:
	python setup.py sdist

check:
	flake8 burin unit examples
