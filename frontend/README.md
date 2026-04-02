# Frontend — GitHub User Insights

Web app built with React 19 + Vite + TypeScript + Tailwind CSS v4 to visualize GitHub user activity metrics.

## Stack

- React 19
- TypeScript
- Vite
- Tailwind CSS v4

## Requirements

- Node.js 18+
- npm 9+

## Installation

```bash
npm install
```

## Development

```bash
npm run dev
```

App available at `http://localhost:5173`.

## Docker

```bash
# All services
docker-compose up --build

# Frontend only
docker-compose up --build frontend
```

App available at `http://localhost:3000`.

## Production build

```bash
npm run build
```

Static files are generated in `dist/`.

## Available scripts

| Script              | Description                        |
|---------------------|------------------------------------|
| `npm run dev`       | Development server with HMR        |
| `npm run build`     | Optimized production build         |
| `npm run preview`   | Preview the local build            |
| `npm run lint`      | Lint with ESLint                   |

## Features

- GitHub user search
- Activity charts (languages, PRs, contributions, hourly activity)
- Internationalization: English and Spanish (EN/ES)
- Light/dark theme toggle
