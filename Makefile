.PHONY: train test lint run docker policy
train:
	python -m src.platform_api.train
test:
	pytest -q
lint:
	ruff check src tests
run:
	uvicorn src.platform_api.api:app --reload
docker:
	docker compose up --build
policy:
	conftest test deploy/kubernetes/base
