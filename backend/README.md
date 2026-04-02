# Backend — GitHub User Insights API

API REST construida con FastAPI que devuelve métricas de actividad de un usuario de GitHub.

## Instalación

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows

pip install -r requirements/requirements.txt
```

## Variables de entorno

Copiar `.env.example` a `.env`:

```bash
cp .env.example .env
```

| Variable              | Descripción                                      | Default                    |
|-----------------------|--------------------------------------------------|----------------------------|
| `GITHUB_TOKEN`        | Personal Access Token de GitHub (requerido)      | —                          |
| `GITHUB_API_URL`      | Base URL de la API de GitHub                     | `https://api.github.com`   |
| `MAX_RESULTS_PER_PAGE`| Resultados por página en paginación              | `100`                      |
| `MAX_PAGES`           | Máximo de páginas a recorrer                     | `5`                        |

### Generar un GitHub Token

1. Ir a [github.com/settings/personal-access-tokens/new](https://github.com/settings/personal-access-tokens/new)
2. Asignar un nombre y fecha de expiración
3. Seleccionar los scopes: `read:user`, `read:org`, `public_repo`
4. Copiar el token generado en el `.env`

## Ejecutar la API

```bash
uvicorn main:app --reload
```

- API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`

## Endpoint

```
GET /user-insights/{username}
```

### Respuesta exitosa (200)

```json
{
  "most_used_languages": [
    {"language": "Python", "count": 10},
    {"language": "JavaScript", "count": 5}
  ],
  "repos_with_more_prs": [
    {"repository": "https://github.com/user/repo1", "count": 3}
  ],
  "monthly_contributions": [
    {"month": "2025-02", "pull_requests": 2, "issues": 3, "commits": 10}
  ],
  "hours_more_activity": [
    {"period": "morning", "count": 5},
    {"period": "afternoon", "count": 8},
    {"period": "evening", "count": 12}
  ]
}
```

### Códigos de respuesta

| Código | Descripción                   |
|--------|-------------------------------|
| 200    | Datos obtenidos correctamente |
| 404    | Usuario de GitHub no encontrado |
| 500    | Error interno del servidor    |

## Tests

```bash
pytest tests/

# Con salida detallada
pytest tests/ -v
```

## Arquitectura

```
main.py (FastAPI router + DI)
    └─ GitHubInsightsService  (src/services/github_insights_service.py)
           ├─ GitHubAPIService  (src/services/github_client_service.py)
           └─ Métricas (src/services/metrics/*.py)
```

### Patrón de métricas

Cada métrica hereda de `BaseGitHubMetric` e implementa `execute(username) -> dict`. El orquestador las descubre dinámicamente con `pkgutil.iter_modules()` y las ejecuta según su atributo `order`.

Para agregar una métrica nueva: crear un archivo en `src/services/metrics/` con una clase que herede de `BaseGitHubMetric`, defina `order: int` e implemente `execute`.
