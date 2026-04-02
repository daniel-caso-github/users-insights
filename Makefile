.DEFAULT_GOAL := help

## ─── Local (uv + npm) ─────────────────────────────────────

local-setup:         ## Install all dependencies (backend + frontend)
	@./scripts/local-setup.sh

local-dev-backend:   ## Run backend with hot-reload (uv)
	@./scripts/local-dev-backend.sh

local-dev-frontend:  ## Run frontend dev server (npm)
	@./scripts/local-dev-frontend.sh

local-test:          ## Run backend tests (uv pytest)
	@./scripts/local-test.sh

## ─── Docker ────────────────────────────────────────────────

docker-build:        ## Build all Docker images
	@./scripts/docker-build.sh

docker-up:           ## Start all services (detached)
	@./scripts/docker-up.sh

docker-down:         ## Stop and remove containers
	@./scripts/docker-down.sh

docker-logs:         ## Tail logs from all services
	@./scripts/docker-logs.sh

## ─── Common ─────────────────────────────────────────────────

help:                ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}'
