project_name = electronic-prescription-service-api-regression-tests

guard-%:
	@ if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set"; \
		exit 1; \
	fi

install-requirements:
	python -m venv .venv
	. .venv/bin/activate && python -m pip install --upgrade pip && \
	python -m pip install poetry && \
	python -m poetry export -f requirements.txt --output requirements.txt && \
	python -m pip install -r requirements.txt

lint-format:
	python -m black .
	python -m pylint . --rcfile=tox.ini


run-tests-exclude-known-bugs: guard-BASE_URL
	echo "Running Regression Tests"
	python runner.py --tags ~bug

