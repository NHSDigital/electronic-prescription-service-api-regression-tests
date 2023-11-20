project_name = electronic-prescription-service-api-regression-tests

guard-%:
	@ if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set"; \
		exit 1; \
	fi

install:
	poetry install --no-root

lint-black:
	python -m black .

lint-pyright:
	python -m pyright .

lint-flake8:
	python -m flake8 .

lint: lint-black lint-pyright lint-flake8

run-tests: guard-BASE_URL
	echo "Running Regression Tests"
	python runner.py

check-licenses:
	scripts/check_python_licenses.sh
