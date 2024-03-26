project_name = electronic-prescription-service-api-regression-tests

guard-%:
	@ if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set"; \
		exit 1; \
	fi

install: install-python install-hooks

install-python:
	poetry install

install-hooks: install-python
	poetry run pre-commit install --install-hooks --overwrite

lint-black:
	poetry run black .

lint-pyright:
	export PYRIGHT_PYTHON_GLOBAL_NODE=on; poetry run pyright .

lint-flake8:
	poetry run flake8 .

lint: lint-black lint-pyright lint-flake8

run-tests: guard-BASE_URL
	echo "Running Regression Tests"
	poetry run python ./runner.py

check-licenses:
	scripts/check_python_licenses.sh

deep-clean-install:
	rm -f -d -r .venv/
	asdf uninstall poetry
	asdf uninstall python
	asdf plugin remove poetry
	asdf plugin remove python
	asdf plugin add python
	asdf install python
	asdf plugin add poetry
	asdf install poetry
	poetry install

pre-commit:
	poetry run pre-commit run --all-files
