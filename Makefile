.PHONY: up down logs seed test
up:
	docker compose up -d --build

down:
	docker compose down -v

logs:
	docker compose logs -f --tail=200

seed:
	python scripts/seed_http.py

test:
	pytest -q
