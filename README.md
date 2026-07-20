# Minimal Django boilerplate

Minimal application for the [Wodby Django service](https://github.com/wodby/service-django) and [Django stack](https://github.com/wodby/stack-django).

The project uses Django 5.2 LTS so it works with every Python version offered by the service. PostgreSQL configuration is read from Wodby's `DB_*` link variables, and static assets are served by WhiteNoise.

## Local development

```shell
uv sync
uv run python manage.py migrate
uv run python manage.py test
uv run python manage.py runserver
```

Open http://localhost:8000. A health endpoint is available at `/healthz`.
