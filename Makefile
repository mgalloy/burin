VERSION=`python setup.py --version`

.PHONY: clean test dist

clean:
	echo "cleaning..."

test:
	python setup.py test

dist:
	python setup.py sdist
