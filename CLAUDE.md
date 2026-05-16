# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the app
uvicorn app.main:app --reload
# or
python -m app.main

# Lint and format (runs automatically as a pre-commit hook)
pre-commit run --all-files

# Run tests
pytest

# Generate a migration after changing models.py
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Roll back one step
alembic downgrade -1

# Run a single test file
pytest tests/test_sources/sources.py
```

Requirements: PostgreSQL running at `localhost:5432`. Copy `.env` settings from the existing `.env` file — `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `SESSION_SECRET_KEY`, `SESSION_MIDDLEWARE_HTTPS_ONLY`.

Alembic is configured in `alembic/`. `env.py` reads DB credentials from `.env` and imports `Base.metadata` from `app/models.py` for autogenerate. Always review generated migration files in `alembic/versions/` before applying.

## Architecture

**Layered MVC**: `Routers → Services → SQLAlchemy ORM → PostgreSQL`

- `app/routers/` — HTTP handlers; render Jinja2 templates or return partial HTML for HTMX swaps
- `app/services/` — Business logic; receives a SQLAlchemy `Session` explicitly (no DI), returns ORM objects
- `app/models.py` — SQLAlchemy 2.0 ORM models (Mapped[T] style)
- `app/schemas.py` — Pydantic v2 models for request validation; `ConfiguredModel` base has `from_attributes=True` for ORM→schema conversion
- `app/deps.py` — FastAPI dependencies: `SessionDepType` (DB session), `UserDep`/`UserDepType` (current authenticated user)
- `app/utils/parse.py` — RSS feed fetching and parsing via `feedparser`
- `app/template.py` — Jinja2 environment setup

**Authentication**: Session-based via `SessionMiddleware` (cookie, 1-hour TTL). `get_current_user_session()` in `deps.py` reads `request.session['user_id']`. Routes that require login raise `RedirectToLogin`, which the global exception handler converts to a redirect to `/users/login`.

**Frontend**: Jinja2 templates + HTMX + Tailwind CSS (CDN, no build step). Templates in `app/templates/`; `partials/` holds HTML fragments returned by HTMX-triggered endpoints. Full-page routes render the complete template; HTMX routes return only the partial.

## Data model

| Table | Key fields |
|---|---|
| `users` | `id`, `username`, `email`, `password_hash` |
| `sources` | `id`, `title`, `feed_link` (UNIQUE, RSS URL), `link` (site URL), `last_etag`, `last_modified` |
| `entries` | `id`, `title`, `link` (UNIQUE), `summary`, `content`, `created_date`, `source_id` FK |
| `user_to_source` | `user_id` + `source_id` (many-to-many join) |

Entry deduplication uses `link` as the unique key (no GUID field currently).

## What's not yet implemented

These are mentioned in `architecture.md` but not in the codebase:
- Alembic migrations
- APScheduler background feed polling
- Async SQLAlchemy (currently sync `Session` + `psycopg2`)
- Per-user read/starred entry status (`user_entry_status` table)
- HTTP conditional requests (ETag/Last-Modified) in feed fetcher

## Code style

Configured in `pyproject.toml`: Ruff, 120-char line length, isort enabled, single quotes. Pre-commit hooks run `ruff check --fix` and `ruff format` on every commit — no need to run style checks manually after edits.
