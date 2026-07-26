# Django starter for Wodby

A production-oriented starter for the [Wodby Django service](https://github.com/wodby/service-django) and [Django stack](https://github.com/wodby/stack-django).

The project uses Django 5.2 LTS so it works with every Python version offered by the service. It includes:

- a conventional Django project and `core` application
- a responsive template and static asset example
- PostgreSQL configuration through Wodby's secret `DATABASE_URL`, with a
  `DB_*` compatibility fallback
- Celery background jobs through a persistent Valkey broker
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

When `DATABASE_URL` is set, it is the authoritative database connection.
Component `DB_*` variables remain supported for compatibility; when neither
form is present, local development uses SQLite.

The stack supplies a secret `CELERY_BROKER_URL` to both the web service and its
Celery worker derivative. `CELERY_APP` selects the boilerplate's `myapp`
package and can be overridden for custom project layouts. `myapp/celery.py`
loads Django settings using Celery's standard `CELERY_*` namespace and
discovers tasks such as the example in `core/tasks.py`. Task results are
intentionally disabled; add a result backend only when the application needs
to retrieve them.

To exercise background jobs locally, start Redis or Valkey and run a worker in
a second terminal:

```shell
export CELERY_APP=myapp
export CELERY_BROKER_URL=redis://localhost:6379/0
uv run celery worker --loglevel=INFO
```

Enqueue the example with
`uv run python manage.py shell -c "from core.tasks import add; add.delay(2, 3)"`.

Valkey is dedicated to queue data and uses persistence with a `noeviction`
policy. The boilerplate does not also use it as Django's cache; add a separate
cache instance when needed. The linked SMTP service is used through
`SMTP_HOST` and `SMTP_PORT` when enabled.

On Wodby, `ALLOWED_HOSTS` is derived from the JSON `WODBY_HOSTS` route list and
the internal `WODBY_APP_SERVICE_NAME`. Set `DJANGO_ALLOWED_HOSTS` to a
comma-separated list to override route-derived hosts outside Wodby.

Wodby terminates TLS and enables HTTPS redirects in its default route settings,
so the starter does not duplicate that redirect in Django. If you deploy behind
another ingress, review Django's `check --deploy` output and configure HTTPS
redirects and HSTS for that environment.
