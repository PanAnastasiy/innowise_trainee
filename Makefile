PROJECT_NAME = innowise_trainee
DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env
CONTAINER_NAME =  docker_compose/pagila_docker/docker-compose.yml


.PHONY: up down rebuild restart status clean logs

up:
	@echo "🚀 Starting Innowise_Trainee containers..."
	${DC} ${ENV} -f  {CONTAINER_NAME}  up -d
	@echo "✅ Containers are up and running."

down:
	@echo "🛑 Stopping $(PROJECT_NAME) containers..."
	${DC} ${ENV} down
	@echo "✅ Containers stopped."

logs:
	@echo "📜 Showing PostgreSQL logs..."
	${LOGS} ${DB_CONTAINER} -f

.PHONY: psql tables

psql:
	@echo "💾 Connecting to PostgreSQL container..."
	@docker ps | grep ${DB_CONTAINER} > /dev/null || (echo "❌ Container ${DB_CONTAINER} not running!"; exit 1)
	${EXEC} ${DB_CONTAINER} psql -U ${PG_USER} -d ${DB_NAME}

tables:
	@echo "📋 Listing tables in database ${DB_NAME}..."
	${EXEC} ${DB_CONTAINER} psql -U ${PG_USER} -d ${DB_NAME} -c '\dt'
