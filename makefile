.DEFAULT_GOAL := turnin

ifeq ($(CI), true)                # Travis CI
    PYTHON   := python
    PIP      := pip3.5
    PYLINT   := pylint
    COVERAGE := coverage-3.5
    PYDOC    := pydoc3
    AUTOPEP8 := autopep8
else                                   # UTCS
    PYTHON   := python
    PIP      := pip3.5
    PYLINT   := pylint3.5
    COVERAGE := coverage-3.5
    PYDOC    := pydoc3.4
    AUTOPEP8 := autopep8
endif

format:
	$(AUTOPEP8) -i app/tests.py 
	$(AUTOPEP8) -i app/__init__.py
	$(AUTOPEP8) -i app/testmodels.py
	$(AUTOPEP8) -i app/testsearch.py

html:
	./html.sh

test: pylint
	./test.sh

log:
	git log > IDB3.log

pylint:
	$(PYLINT) app/models.py

turnin: format test html log
	echo "this is the turnin make target"

clean:
	rm -f app/tests.out
	rm -f *.pyc app/*.pyc
	rm -f *.html
	rm -f *.log



# lint:
# 	find . -type f \( -name "*.py" -and -not -name "*_test.py" \) | xargs pylint -r n

# run:
# 	python sweapplication/application.py
