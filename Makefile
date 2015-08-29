all: test

ifeq ($(OSNAME), Linux)
OPEN_COMMAND		:= gnome-open
else
OPEN_COMMAND		:= open
endif

test: clean unit functional documentation

deps:
	pip install -U pip
	pip install -r requirements.txt

unit:
	@nosetests -v -s --rednose --with-coverage --cover-erase --cover-package=repocket tests/unit

functional:
	@nosetests --stop --logging-level=INFO -v -s --with-coverage --cover-erase --cover-package=repocket --rednose tests/functional

clean:
	@rm -rf sandbox dist
	@git clean -Xdf

release: clean
	./.release

documentation:
	cd docs && make html
	#$(OPEN_COMMAND) docs/build/html/index.html
