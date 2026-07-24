# Django starter for Wodby

A production-oriented starter for the [Wodby Django service](https://github.com/wodby/service-django) and [Django stack](https://github.com/wodby/stack-django).

The project uses Django 5.2 LTS so it works with every Python version offered by the service. It includes:

- a conventional Django project and `core` application
- a responsive template and static asset example
- PostgreSQL configuration through Wodby's `DB_*` link variables
- Gunicorn and WhiteNoise for production serving
- Wodby CI build, release, deployment, and post-deployment checks
- a lightweight health endpoint at `/healthz`

## Local development

```shell
uv sync
export DJANGO_DEBUG=true
uv run python manage.py migrate
uv run python manage.py test
uv run python manage.py runserver
```

Open http://localhost:8000. A health endpoint is available at `/healthz`.

## Start building

The `myapp` package contains project-level configuration. The `core` package is
a small Django application that owns the landing page and health endpoint.

Create another application for your product domain:

```shell
uv run python manage.py startapp products
```

Add its application config to `INSTALLED_APPS` in `myapp/settings.py`, then
include its URL configuration from `myapp/urls.py`.

To use the built-in Django administration site locally, create a user and open
http://localhost:8000/admin/:

```shell
uv run python manage.py createsuperuser
```

Wodby injects a generated `DJANGO_SECRET_KEY` into deployed applications.
Outside Wodby, set `DJANGO_SECRET_KEY` whenever `DJANGO_DEBUG` is disabled.
Set `DJANGO_ALLOWED_HOSTS` to a comma-separated host list when the application
is not protected by Wodby's route gateway.

Wodby terminates TLS and enables HTTPS redirects in its default route settings,
so the starter does not duplicate that redirect in Django. If you deploy behind
another ingress, review Django's `check --deploy` output and configure HTTPS
redirects and HSTS for that environment.
