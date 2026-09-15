# AGENTS.md

## Project

LangGraphInAction is an agentic AI application. Core stack:

- **LangGraph** — stateful, multi-agent graph orchestration
- **FastAPI** — HTTP/streaming API layer
- **Temporal** — durable workflows and activities
- **Qdrant** — vector store for retrieval (RAG)
- **PostgreSQL** — persistence, checkpoints, app data
- **Playwright** — browser automation / scraping tools
- **uv** — dependency and environment management

## Toolchain

After **every code change**, run lint and static type analysis before considering the
task complete:

```bash
uv run ruff check .
uv run ruff format .
uv run mypy .
```

Auto-fix lint issues where safe:

```bash
uv run ruff check . --fix
```

`mypy` runs in `strict` mode; new code must be fully typed (return annotations included).

## Testing

```bash
uv run pytest
```

## Dependency management

- Runtime deps go in `[project.dependencies]`; dev-only tooling goes in the
  `[dependency-groups] dev` group in `pyproject.toml`.
- `dev` is a default group, so plain `uv sync` installs it for local work.
- Production installs use `uv sync --frozen --no-dev`.
- Add packages with `uv add <pkg>` or `uv add --dev <pkg>`; commit `uv.lock`.

## Conventions

- Python 3.14, line length 100 (configured in `pyproject.toml`).
- Do not add comments unless asked.
- Never commit `.env` or secrets; use `.env.example` for templates.
