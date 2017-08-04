all: test documentation

ifeq ($(OSNAME), Linux)
OPEN_COMMAND		:= gnome-open
else
OPEN_COMMAND		:= open
endif

test: clean unit functional

deps:
	pip install -U pip
	pip install -r requirements.txt

unit:
	@nosetests -x -v -s --rednose --with-coverage --cover-erase --cover-package=repocket tests/unit

functional:
	@nosetests --stop --logging-level=INFO -v -s --with-coverage --cover-erase --cover-package=repocket --rednose tests/functional

clean:
	@rm -rf sandbox dist
	@git clean -Xdf

release: clean
	@rm -rf dist
	@python setup.py sdist
	@twine upload dist/*.tar.gz

html-docs:
	cd docs && make html

docs: html-docs
	$(OPEN_COMMAND) docs/build/html/index.html
