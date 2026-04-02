# GitHub User Insights

Monorepo with a REST API (FastAPI) and a web app (React + Vite) to visualize GitHub user activity metrics.

## Structure

```
users-insights/
├── backend/    ← FastAPI API
└── frontend/   ← React + Vite + TypeScript app
```

## Quick start

### Backend

```bash
cd backend
pip install -r requirements/requirements.txt
cp .env.example .env   # set GITHUB_TOKEN
uvicorn main:app --reload
```

API available at `http://localhost:8000` — docs at `http://localhost:8000/docs`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App available at `http://localhost:5173`.

## Documentation

- [Backend](backend/README.md) — installation, environment variables, endpoint, tests and architecture
- [Frontend](frontend/README.md) — requirements, available scripts and production build
