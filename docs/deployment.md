# Deployment Guide

Guide for deploying Quiz Forge to production.

---

## Docker Compose (Recommended)

### 1. Build production images

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml build
```

### 2. Configure environment

Create a `.env` file in the project root with production values:

```env
SECRET_KEY=<generate-a-strong-random-key>
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key
DATABASE_URL=postgresql://user:pass@host:5432/quiz_forge
CORS_ORIGINS=https://your-domain.com
DEBUG=false
LOG_LEVEL=WARNING
```

### 3. Deploy

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### 4. Verify

```bash
curl http://localhost:8000/health
```

---

## Docker Image Details

### Backend

- **Base**: `python:3.11-slim`
- **Multi-stage**: Builder installs deps → runtime copies virtualenv only
- **User**: Non-root `appuser` (UID 1001)
- **Health check**: `curl http://localhost:8000/health`
- **Resource limits**: 512MB RAM, 0.5 CPU (configurable in compose)

### Frontend

- **Base**: `node:18-alpine`
- **Multi-stage**: Builder runs `next build` → runtime copies standalone output
- **User**: Non-root `nextjs` (UID 1001)
- **Health check**: `curl http://localhost:3000`
- **Output**: Next.js standalone mode (no `node_modules` in runtime)

---

## Environment Variables

| Variable                  | Required | Default              | Description                  |
|---------------------------|----------|----------------------|------------------------------|
| `SECRET_KEY`              | Yes      | —                    | JWT signing key              |
| `SUPABASE_URL`            | No       | —                    | Supabase project URL         |
| `SUPABASE_KEY`            | No       | —                    | Supabase anon/service key    |
| `DATABASE_URL`            | No       | —                    | PostgreSQL connection string |
| `API_HOST`                | No       | `0.0.0.0`            | Backend bind host            |
| `API_PORT`                | No       | `8000`               | Backend bind port            |
| `CORS_ORIGINS`            | No       | `http://localhost:3000` | Comma-separated origins   |
| `DEBUG`                   | No       | `false`              | Enable debug mode            |
| `LOG_LEVEL`               | No       | `INFO`               | Python log level             |
| `RATE_LIMIT_PER_MINUTE`   | No       | `60`                 | API rate limit per IP        |
| `SENTRY_DSN`              | No       | —                    | Sentry error tracking DSN    |

---

## Monitoring

### Prometheus Metrics

Metrics are exposed at `/metrics` when `prometheus-fastapi-instrumentator` is installed.

Key metrics:
- `http_requests_total` — request count by method, path, and status
- `http_request_duration_seconds` — request latency histogram
- `http_request_size_bytes` — request body size
- `http_response_size_bytes` — response body size

### Health Check

`GET /health` returns:

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "api_version": "v1",
  "environment": "production"
}
```

---

## Security Checklist

- [ ] `SECRET_KEY` is a strong random value (not the default)
- [ ] `DEBUG` is `false` in production
- [ ] `CORS_ORIGINS` is set to your actual domain(s)
- [ ] Docker images are scanned with Trivy (runs in CI)
- [ ] Dependencies are audited with `pip-audit` (runs in CI)
- [ ] Rate limiting is enabled (60 req/min default)
- [ ] Containers run as non-root users

---

## CI/CD

GitHub Actions workflows handle:

1. **backend-ci.yml** — Lint, test, security scan, Docker build + Trivy
2. **frontend-ci.yml** — Lint, test, build, Docker build
3. **integration.yml** — Full stack smoke test on push to `main`

Deploy after all checks pass on `main`.
