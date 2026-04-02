# GitHub User Insights

Monorepo with a REST API (FastAPI) and a web app (React + Vite) to visualize GitHub user activity metrics.

## Demo

<video src="docs/demo.mp4" controls width="100%"></video>

## Tech Stack

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![uv](https://img.shields.io/badge/uv-DE5FE9?logo=astral&logoColor=white)
![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?logo=typescript&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-v4-06B6D4?logo=tailwindcss&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-646CFF?logo=vite&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) — for the Docker/Makefile workflow
- [uv](https://docs.astral.sh/uv/) — for local backend development
- [Node.js 18+](https://nodejs.org/) — for local frontend development

## Structure

```
users-insights/
├── backend/    ← FastAPI API
└── frontend/   ← React + Vite + TypeScript app
```

## Docker

Start all services with a single command:

```bash
docker-compose up --build
```

| Service  | URL                        |
|----------|----------------------------|
| Backend  | `http://localhost:8000`    |
| Frontend | `http://localhost:3000`    |

## Makefile

```bash
make local-setup          # Install all dependencies (backend + frontend)
make local-dev-backend    # Run backend with hot-reload
make local-dev-frontend   # Run frontend dev server
make local-test           # Run backend tests
make docker-up            # Start all services (detached)
make docker-down          # Stop and remove containers
make docker-logs          # Tail logs from all services
```

## Documentation

- [Backend](backend/README.md) — installation, environment variables, endpoint, tests and architecture
- [Frontend](frontend/README.md) — requirements, available scripts and production build
