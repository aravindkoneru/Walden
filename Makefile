PYTHON = python3.8

.PHONY: test
test:
	${PYTHON} -m pytest tests/

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
