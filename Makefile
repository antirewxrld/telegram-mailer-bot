.PHONY: up
up: ## Поднять контейнеры (detached)
	@echo "🚀 Поднимаем контейнеры (detached)..."
	docker compose up -d --build

.PHONY: up-follow
up-follow: ## Поднять контейнеры с логами
	@echo "📡 Поднимаем контейнеры (в консоли)..."
	docker compose up --build

.PHONY: down
down: ## Остановить и удалить контейнеры
	@echo "🛑 Останавливаем и удаляем контейнеры..."
	docker compose down

.PHONY: reload
reload: ## Перезапустить контейнеры (detached)
	@$(MAKE) down
	@$(MAKE) up

.PHONY: reload-follow
reload-follow: ## Перезапустить контейнеры с логами
	@$(MAKE) down
	@$(MAKE) up-follow

.PHONY: logs
logs: ## Смотреть логи контейнеров
	@echo "📖 Просмотр логов контейнеров..."
	docker compose logs -f

.PHONY: ps
ps: ## Показать запущенные контейнеры	
	@echo "📋 Список запущенных контейнеров..."
	docker compose ps

.PHONY: update
update: ## Обновить бота
	@echo "🔄 Обновляем бота..."
	git pull origin main

.PHONY: update-reload
update-reload: ## Обновить бота с перезапуском
	@echo "🔄 Обновляем бота..."
	git pull origin main
	@echo "🚀 Перезапускаем контейнеры..."
	@$(MAKE) reload

.PHONY: help
help: ## Показать список доступных команд
	@echo ""
	@echo "📘 Команды Makefile:"
	@echo ""
	@awk -F':.*## ' '/^[a-zA-Z0-9_-]+:.*## / {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""