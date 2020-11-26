PYTHON = python3

.PHONY: test
test:
	${PYTHON} -m pytest tests/

.PHONY: build
build:
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
	rm -rf resources/ dist/ build/ walden.egg-info/
