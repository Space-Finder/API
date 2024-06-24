run:
	@DEVMODE=false python src/main.py

dev:
	@DEVMODE=true python src/main.py

clean:
	@find . | grep -E '(__pycache__|\.pyc|\.pyo$|\.DS_Store)' | xargs rm -rf

format:
	@black src/

lint:
	@flake8 src/

setup:
	@python src/setup.py