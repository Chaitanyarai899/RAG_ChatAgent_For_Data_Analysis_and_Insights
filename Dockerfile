# The builder image, used to build the virtual environment
FROM python:3.11-slim-buster as builder

RUN apt-get update && apt-get install -y git

RUN pip install poetry==1.4.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

ENV HOST=0.0.0.0
ENV LISTEN_PORT 8000
EXPOSE 8000

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

# The runtime image, used to just run the code provided its virtual environment
FROM python:3.11-slim-buster as runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY ./RAG_Logic ./RAG_Logic
COPY ./.chainlit ./.chainlit
COPY chainlit.md ./

WORKDIR ./RAG_Logic

CMD ["chainlit", "run", "main.py"]
