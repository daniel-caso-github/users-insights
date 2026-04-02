# GitHub User Insights

Monorepo con una API REST (FastAPI) y una app web (React + Vite) para visualizar métricas de actividad de usuarios de GitHub.

## Estructura

```
users-insights/
├── backend/    ← API FastAPI
└── frontend/   ← App React + Vite + TypeScript
```

## Quick start

### Backend

```bash
cd backend
pip install -r requirements/requirements.txt
cp .env.example .env   # configurar GITHUB_TOKEN
uvicorn main:app --reload
```

API disponible en `http://localhost:8000` — docs en `http://localhost:8000/docs`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App disponible en `http://localhost:5173`.

## Documentación

- [backend/README.md](backend/README.md) — instalación, variables de entorno, endpoint, tests y arquitectura
- [frontend/README.md](frontend/README.md) — requisitos, scripts disponibles y build de producción
