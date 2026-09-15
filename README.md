# LangGraphInAction

An agentic AI application built with **LangGraph**, exposed via **FastAPI**, orchestrated with **Temporal**, using **Qdrant** for vector search, **PostgreSQL** for persistence, and **Playwright** for browser automation.

## Stack

| Layer            | Technology   | Purpose                                          |
| ---------------- | ------------ | ------------------------------------------------ |
| Agent framework  | LangGraph    | Stateful, multi-agent graph orchestration        |
| API              | FastAPI      | HTTP interface and streaming endpoints           |
| Orchestration    | Temporal     | Durable, long-running workflows and retries      |
| Vector store     | Qdrant       | Semantic search and retrieval (RAG)              |
| Database         | PostgreSQL   | Durable state, checkpoints, and app data         |
| Browser tooling  | Playwright   | Web scraping and browser-based agent tools       |
| Dependency mgmt  | uv           | Fast, reproducible Python environments           |

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- Docker / Docker Compose (for Postgres, Qdrant, Temporal)

## Getting Started

Clone the repository and install dependencies:

```bash
git clone <repo-url>
cd LangGraphInAction
uv sync
```

Run Playwright browser install (first time only):

```bash
uv run playwright install --with-deps
```

## Environment

Copy the example env file and fill in your values:

```bash
cp .env.example .env
```

Typical variables:

```dotenv
# App
APP_ENV=local
LOG_LEVEL=info

# API
HOST=0.0.0.0
PORT=8000

# Postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=langgraph
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/langgraph

# Qdrant
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=

# Temporal
TEMPORAL_HOST=localhost:7233
TEMPORAL_NAMESPACE=default
TEMPORAL_TASK_QUEUE=langgraph-tasks

# Model providers
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
```

## Infrastructure

Start backing services with Docker Compose:

```bash
docker compose up -d postgres qdrant temporal
```

| Service  | URL                     |
| -------- | ----------------------- |
| FastAPI  | http://localhost:8000   |
| Postgres | localhost:5432          |
| Qdrant   | http://localhost:6333   |
| Temporal | http://localhost:8233   |

## Running

Start the API (dev, with reload):

```bash
uv run uvicorn app.main:app --reload
```

Start the Temporal worker:

```bash
uv run python -m app.worker
```

## Project Layout

```
.
├── app/
│   ├── main.py          # FastAPI application entrypoint
│   ├── worker.py        # Temporal worker entrypoint
│   ├── api/             # HTTP routes
│   ├── graph/           # LangGraph agents, nodes, and state
│   ├── workflows/       # Temporal workflows and activities
│   ├── tools/           # Agent tools (Playwright, retrieval, etc.)
│   ├── db/              # Postgres models and migrations
│   ├── vector/          # Qdrant client and collections
│   └── core/            # Config, logging, settings
├── tests/
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── uv.lock
```

## Development

Dev tooling (ruff, mypy) lives in the uv `dev` dependency group, which is installed
by default with `uv sync`. Production installs must exclude it:

```bash
uv sync --frozen --no-dev
```

Run checks locally:

```bash
uv run ruff check .
uv run ruff format .
uv run mypy .
uv run pytest
```

## Docker

Build and run the full stack:

```bash
docker compose up --build
```

Production images should install runtime dependencies only:

```dockerfile
RUN uv sync --frozen --no-dev
```

## License

See [LICENSE](LICENSE) if present.
