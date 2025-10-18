PROJECT_NAME = innowise_trainee
DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env
CONTAINER_NAME =  docker_compose/pagila_docker/docker-compose.yml


.PHONY: up
up:
	@echo "Starting $(PROJECT_NAME) containers..."
	${DC} ${ENV} -f  {CONTAINER_NAME}  up -d
	@echo "Containers are up and running."

.PHONY: down
down:
	@echo "Stopping $(PROJECT_NAME) containers..."
	${DC} ${ENV} down
	@echo "Containers stopped."

.PHONY: logs
logs:
	@echo "Showing PostgreSQL logs..."
	${LOGS} ${DB_CONTAINER} -f