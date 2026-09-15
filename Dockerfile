FROM python:3.13-alpine AS builder

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev

COPY src ./src

FROM python:3.13-alpine AS production

WORKDIR /app

COPY --from=builder /app/.venv ./.venv
COPY --from=builder /app/src ./src

ENV PATH="/app/.venv/bin:$PATH"

CMD ["uvicorn", "src.main:create_app", "--host", "0.0.0.0", "--port", "8000"]
