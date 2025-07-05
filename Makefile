project_name = electronic-prescription-service-api-regression-tests

.PHONY: test

guard-%:
	@ if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set"; \
		exit 1; \
	fi

install: install-python install-hooks install-node

install-full: clear-virtualenv install-asdf install install-playwright

uninstall-full: clear-virtualenv asdf-uninstall

update: update-poetry update-node install

update-node:
	npm update

update-poetry:
	poetry update

install-asdf:
	asdf plugin add python
	asdf plugin add poetry
	asdf plugin add shellcheck
	asdf plugin add nodejs
	asdf plugin add actionlint
	asdf plugin add allure
	asdf install

install-python:
	poetry install

install-hooks: install-python
	poetry run pre-commit install --install-hooks --overwrite

install-playwright:
	playwright install
	playwright install-deps
	playwright install --force chrome

install-node:
	npm ci

lint-black:
	poetry run black .

lint-pyright:
	export PYRIGHT_PYTHON_GLOBAL_NODE=0; poetry run pyright .

lint-flake8:
	poetry run flake8 .

lint: lint-black lint-pyright lint-flake8

run-tests: guard-product guard-env
	echo "Running Regression Tests"
	poetry run python ./runner.py --product=$(product) --env=$(env) --tags=$(tags) --arm64=${arm64}

check-licenses:
	scripts/check_python_licenses.sh

clear-virtualenv:
	rm -f -d -r .venv/
	mkdir .venv/

asdf-uninstall:
	asdf plugin remove poetry
	asdf plugin remove python
	asdf plugin remove shellcheck
	asdf plugin remove nodejs
	asdf plugin remove actionlint
	asdf plugin remove allure

deep-clean-install:
	make clear-virtualenv
	make asdf-uninstall
	make install-full

pre-commit: git-secrets-docker-setup
	poetry run pre-commit run --all-files

git-secrets-docker-setup:
	export LOCAL_WORKSPACE_FOLDER=$(pwd)
	docker build -f https://raw.githubusercontent.com/NHSDigital/eps-workflow-quality-checks/refs/tags/v4.0.4/dockerfiles/nhsd-git-secrets.dockerfile -t git-secrets .

download-allure-report: guard-GITHUB_RUN_ID
	rm -rf allure-report
	rm -rf allure-results
	gh run download ${GITHUB_RUN_ID}
	allure generate
	allure open
