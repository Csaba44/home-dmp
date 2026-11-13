FROM python:3.11.18-alpine3.23@sha256:3e6740f02c2a48bfcf675c39ae0f456153667d9d87c1e5bb2e13ff848dba307f AS base

WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

FROM base AS dev
COPY requirements-dev.txt .
RUN python -m pip install -r requirements-dev.txt
CMD ["watchfiles", "python /app/main.py", "/app"]
