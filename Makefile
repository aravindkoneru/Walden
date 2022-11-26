PYTHON = /usr/local/bin/python

.PHONY: test
test:
	${PYTHON} -m pytest --cov-report term-missing --cov=walden tests/

.PHONY: build
build: clean
	poetry build

.PHONY: publish 
publish: build
	poetry publish

.PHONY: publish-dev
publish-dev: build
	poetry config repositories.testpypi https://test.pypi.org/legacy/
	poetry publish -r testpypi

.PHONY: clean 
clean:
	rm -rf dist/
