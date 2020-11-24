PYTHON = python3

.PHONY: test
test:
	${PYTHON} -m pytest tests/

.PHONY: build
build:
	${PYTHON} setup.py sdist bdist_wheel

.PHONY: publish 
publish: build
	${PYTHON} -m twine upload dist/*

.PHONY: publish-dev
publish-dev: build
	${PYTHON} -m twine upload --repository testpypi dist/*

.PHONY: clean 
clean:
	rm -rf resources/ dist/ build/ walden.egg-info/
