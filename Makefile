# Define the default target
.DEFAULT_GOAL := help

# Variables
COMPOSE_FILE := docker-compose.yaml

# Targets
.PHONY: up down logs clean help

up: ## Start the containers
	docker-compose up --build

down: ## Stop and remove the containers
	docker-compose -f $(COMPOSE_FILE) down
	docker system prune -a
	docker volume prune -f


logs: ## View the container logs
	sudo docker-compose -f $(COMPOSE_FILE) logs -f

clean: ## Remove all containers, networks, and volumes
	sudo docker-compose -f $(COMPOSE_FILE) down -v --remove-orphans

help: ## Display this help message
	@echo "Available targets:"
	@awk '/^[a-zA-Z\-\_0-9]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = $$1; \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "  \033[36m%-20s\033[0m %s\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)