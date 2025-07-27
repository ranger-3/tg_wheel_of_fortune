ARG PYTHON_VERSION="3.13"
ARG WORKDIR_PATH="/app"
ARG VIRTUAL_ENV="/app/.venv"

FROM ghcr.io/astral-sh/uv:python${PYTHON_VERSION}-bookworm-slim AS build

ARG WORKDIR_PATH
WORKDIR ${WORKDIR_PATH}

ENV UV_COMPILE_BYTECODE=1

ENV UV_LINK_MODE=copy

RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv sync --frozen --no-install-project --no-dev

COPY . .


FROM python:${PYTHON_VERSION}-slim AS final

ARG WORKDIR_PATH
ARG VIRTUAL_ENV

RUN useradd -mu 1000 node
USER node

ENV VIRTUAL_ENV=${VIRTUAL_ENV}

WORKDIR "${WORKDIR_PATH}"

COPY --chown=node --from=build ${WORKDIR_PATH} ${WORKDIR_PATH}
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

RUN mkdir -p "/${WORKDIR_PATH}/logs" && chown -R node:node "/${WORKDIR_PATH}/logs"

ENTRYPOINT ["python3", "app.py"]
