# TODO: make sure all commands run even if they exit with non-zero

test:
	@echo "==== Running nosetests ===="
	@nosetests
	@echo "==== Running Flake8 ===="
	@flake8 *.py
	@flake8 mrbob
