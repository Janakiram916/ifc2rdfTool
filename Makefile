SRC_PATH := ".\ifc2rdfTool"

.PHONY: install
install: ## Installs all dependencies
	poetry install

.PHONY: requirements.txt
requirements.txt: ## Creates requirements.txt file
	poetry export -f requirements.txt --output requirements.txt

.PHONY: lint
lint: ## Execute lint script located in the bin folder of the dt/config repo
	poetry run pylint $(SRC_PATH)

.PHONY: auto-format
auto-format: ## Automatically formats the code
	poetry run black $(SRC_PATH) ./tests
	poetry run isort $(SRC_PATH) ./tests

.PHONY: test
test:
	poetry run pytest -vvv -s $(SRC_PATH) ./tests --disable-pytest-warnings

.PHONY: check
check: auto-format lint test ## Runs all code checks and tests
