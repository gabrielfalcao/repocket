all: test documentation

ifeq ($(OSNAME), Linux)
OPEN_COMMAND		:= gnome-open
else
OPEN_COMMAND		:= open
endif

test: clean lint unit functional

deps:
	@(2>&1 which pipenv > /dev/null) || pip install pipenv
	@pipenv install --dev --skip-lock

lint:
	@flake8 repocket

unit:
	@pipenv run nosetests -x -v -s --rednose --with-coverage --cover-erase --cover-package=repocket tests/unit

functional:
	@pipenv run nosetests --stop --logging-level=INFO -v -s --with-coverage --cover-erase --cover-package=repocket --rednose tests/functional

clean:
	@rm -rf sandbox dist
	@git clean -Xdf

release: tests
	@./.release
	@rm -rf dist
	@pipenv run python setup.py sdist
	@pipenv run twine upload dist/*.tar.gz

html-docs:
	cd docs && make html

docs: html-docs
	$(OPEN_COMMAND) docs/build/html/index.html
