project_name = electronic-prescription-service-api-regression-tests

guard-%:
	@ if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set"; \
		exit 1; \
	fi

install:
	poetry install

lint-black:
	python -m black .

lint-pylint:
	python -m pylint . --rcfile=.pylintrc

lint: lint-black lint-pylint

run-tests: guard-BASE_URL
	echo "Running Regression Tests"
	python runner.py

check-licenses:
	scripts/check_python_licenses.sh
