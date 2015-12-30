VERSION=`python setup.py --version`

.PHONY: clean dist test unit

clean:
	echo "cleaning..."

test:
	python setup.py test

unit:
	python setup.py test

dist:
	python setup.py sdist
