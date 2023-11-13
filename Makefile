project_name = electronic-prescription-service-api-regression-tests

guard-%:
	@ if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set"; \
		exit 1; \
	fi

install:
	poetry install
lint-format:
	python -m black .
	python -m pylint . --rcfile=tox.ini


run-tests: guard-BASE_URL
	echo "Running Regression Tests"
	python runner.py

check-licenses:
	scripts/check_python_licenses.sh
