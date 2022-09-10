test:
	pytest tests/

quality_checks:
	isort .
	black .
	pylint --recursive=y integration_test.py

integration_test: quality_checks test
	bash run_test.sh

setup:
	pipenv install --dev
	pre-commit install
