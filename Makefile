PROJECT_NAME = innowise_trainee
DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env
COMPOSE_FILE = docker_compose/snowflake_docker/docker-compose.yml

DB_CONTAINER := pagila_postgres

.PHONY: up
up:
	@echo "Starting $(PROJECT_NAME) containers..."
	$(DC) $(ENV) -f $(COMPOSE_FILE) up -d
	@echo "Containers are up and running."

.PHONY: down
down:
	@echo "Stopping $(PROJECT_NAME) containers..."
	$(DC) $(ENV) -f $(COMPOSE_FILE) down
	@echo "Containers stopped."

.PHONY: logs
logs:
	@echo "Showing PostgreSQL logs..."
	$(LOGS) $(DB_CONTAINER) -f


# Poetry / Development commands

.PHONY: install
install:
	@echo "Installing all dependencies (runtime + dev)..."
	poetry install --with dev

.PHONY: shell
shell:
	@echo "Activating Poetry shell..."
	poetry shell

.PHONY: black
black:
	@echo "Running Black formatter (check mode)..."
	poetry run black --check .

.PHONY: black-fix
black-fix:
	@echo "Running Black formatter (fix mode)..."
	poetry run black .

.PHONY: flake8
flake8:
	@echo "Running Flake8..."
	poetry run flake8 .

.PHONY: isort
isort:
	@echo "Running isort..."
	poetry run isort --check-only .

.PHONY: isort-fix
isort-fix:
	@echo "Fixing import order with isort..."
	poetry run isort .

.PHONY: lint
lint: black flake8 isort
	@echo "All linting checks passed!"

.PHONY: pre-coomit
pre-commit: black flake8 isort
	poetry run pre-commit run --all-files
