FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml /app/
RUN pip install --no-cache-dir uv && \
    uv pip install -e .

COPY . /app

ENV APP_ENV=prod APP_APP_NAME=fastapi-min APP_DEBUG=false

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]


