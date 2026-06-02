.PHONY: test-unit test-e2e lint

test-unit:
	uv run python -m unittest discover -s ./async_include/tests/unit

test-e2e:
	docker compose -f async_include/tests/e2e/docker-compose.yml up --build --exit-code-from test-runner

lint:
	uv run black --check async_include
	uv run ruff check async_include
	uv run mypy async_include
