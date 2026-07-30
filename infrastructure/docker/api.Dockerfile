FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml ./
COPY apps/api ./apps/api
COPY packages ./packages
COPY platform ./platform
COPY engines ./engines
COPY infrastructure ./infrastructure

RUN pip install --no-cache-dir .

EXPOSE 8000

ENTRYPOINT ["/app/infrastructure/docker/api-entrypoint.sh"]
CMD ["uvicorn", "callibr_api.main:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
