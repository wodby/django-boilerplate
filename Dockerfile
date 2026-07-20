ARG WODBY_BASE_IMAGE
FROM ${WODBY_BASE_IMAGE}

ENV UV_COMPILE_BYTECODE=1 \
    UV_NO_CACHE=1 \
    PATH="/usr/src/app/.venv/bin:${PATH}"

ARG COPY_FROM
COPY --chown=wodby:wodby ${COPY_FROM}/pyproject.toml ${COPY_FROM}/uv.lock /usr/src/app/
RUN uv sync --frozen --no-dev --no-install-project

COPY --chown=wodby:wodby ${COPY_FROM} /usr/src/app
RUN uv sync --frozen --no-dev && \
    DJANGO_SECRET_KEY=build-only python manage.py collectstatic --no-input
