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


run-tests: guard-BASE_URL
	echo "Running Regression Tests"
	python runner.py

check-licenses: check-licenses-node check-licenses-python check-licenses-go

check-licenses-node:
	npm run check-licenses
	npm run check-licenses --workspace packages/getMyPrescriptions
	npm run check-licenses --workspace packages/capabilityStatement
	npm run check-licenses --workspace packages/sandbox
	npm run check-licenses --workspace packages/middleware
	npm run check-licenses --workspace packages/splunkProcessor
	npm run check-licenses --workspace packages/statusLambda
	npm run check-licenses --workspace packages/spineClient

check-licenses-python:
	scripts/check_python_licenses.sh

check-licenses-go:
	cd packages/getSecretLayer && ./check_licence.sh

