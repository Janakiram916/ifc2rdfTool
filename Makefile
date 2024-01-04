SRC_PATH := ".\ifc2rdfTool"

.PHONY: install
install: ## Installs all dependencies
	poetry install

.PHONY: requirements.txt
requirements.txt: ## Creates requirements.txt file
	poetry export -f requirements.txt --output requirements.txt --without-hashes

.PHONY: lint
lint: ## Execute lint script located in the bin folder of the dt/config repo
	poetry run pylint $(SRC_PATH)

.PHONY: auto-format
auto-format: ## Automatically formats the code
	poetry run black $(SRC_PATH) ./tests
	poetry run isort $(SRC_PATH) ./tests

.PHONY: unit-test
unit-test:
	poetry run pytest -vvv -s $(SRC_PATH) ./tests/unit_test --disable-pytest-warnings

.PHONY: integration-test
integration-test:
	poetry run pytest -vvv -s $(SRC_PATH) ./tests/integration_test --disable-pytest-warnings

.PHONY: test
test: unit-test integration-test ## Runs all tests

.PHONY: check
check: auto-format lint test requirements.txt ## Runs all code checks and tests

.PHONY: app
app:
	poetry run flet ifc2rdfApp