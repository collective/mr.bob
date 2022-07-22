test: nosetests flake8

nosetests:
	@echo "==== Running nosetests ===="
	@nose2 -v

flake8:
	@echo "==== Running Flake8 ===="
	@flake8 mrbob *.py
