PYTHON = python3

.PHONY: test
test:
	${PYTHON} -m pytest tests/

.PHONY: build
build: clean
	python setup.py sdist bdist_wheel

.PHONY: publish 
publish: build
	twine upload dist/*

.PHONY: publish-dev
publish-dev: build
	twine upload --repository testpypi dist/*

.PHONY: clean 
clean:
	rm -rf resources/ dist/ build/ walden.egg-info/
