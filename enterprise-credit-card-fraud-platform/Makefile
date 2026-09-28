install:
	pip install -r requirements-dev.txt
sample:
	python scripts/generate_sample_data.py
run:
	python -m fraud_detection.cli run-all --input data/samples/sample_transactions.csv
test:
	pytest
lint:
	ruff check .
format:
	ruff format .
api:
	uvicorn api.main:app --reload
docker-up:
	docker compose up --build
