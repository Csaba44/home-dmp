FROM python:3.11.18-alpine3.23@sha256:3e6740f02c2a48bfcf675c39ae0f456153667d9d87c1e5bb2e13ff848dba307f AS base

WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

FROM base AS dev
COPY requirements-dev.txt .
RUN python -m pip install -r requirements-dev.txt
CMD ["watchfiles", "python /app/src/main.py", "/app"]

FROM python:3.11-slim-bookworm@sha256:a83ba18aef0f865b1a4a611c2cf460fe446f2795673bbb9fe43be570439e3b39 AS build
WORKDIR /build

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN python -m pip install -r requirements.txt pyinstaller

COPY . .

RUN apt-get update \
  && apt-get install -y binutils
RUN pyinstaller main.spec

FROM scratch AS export
COPY --from=build /build/dist/main/homefloor-notifications /