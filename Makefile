ARGS ?=

.PHONY: dev prod test help

help: ## Show available targets
	@echo "Usage:"
	@echo "  make dev  [ARGS=\"...\"]  — run in DEV mode  (MockLLM, no API calls)"
	@echo "  make prod [ARGS=\"...\"]  — run in PROD mode (real Claude API)"
	@echo "  make test               — run test suite in DEV mode"
	@echo ""
	@echo "Examples:"
	@echo "  make dev  ARGS=\"review t redis\""
	@echo "  make dev  ARGS=\"mock --tag sliding_window\""
	@echo "  make prod ARGS=\"review t 索引\""
	@echo "  make test"

dev: ## Run app in DEV mode (no real API calls)
	APP_ENV=dev python3 -m app $(ARGS)

prod: ## Run app in PROD mode (requires ANTHROPIC_API_KEY in .env)
	APP_ENV=prod python3 -m app $(ARGS)

test: ## Run test suite in DEV mode
	APP_ENV=dev python3 -m pytest tests/ -v
