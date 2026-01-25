FROM python:3.10-alpine AS base

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN apk add --no-cache gcc musl-dev
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

COPY . .

EXPOSE 8000
COPY scripts/script.sh ./scripts/script.sh

CMD ["bin/bash", "scripts/script.sh"]`