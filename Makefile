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
