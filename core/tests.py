import os
from unittest.mock import patch

from django.test import SimpleTestCase, override_settings
from django.urls import reverse

from core.tasks import add
from myapp.settings import get_allowed_hosts

TEST_STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
    },
}


@override_settings(STORAGES=TEST_STORAGES)
class ViewsTest(SimpleTestCase):
    def test_index(self):
        response = self.client.get(reverse("core:index"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/index.html")
        self.assertContains(response, "Your Django app is running")

    def test_healthz(self):
        response = self.client.get(reverse("core:healthz"))

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "ok"})


class TasksTest(SimpleTestCase):
    def test_add(self):
        self.assertEqual(add.run(2, 3), 5)


@override_settings(STORAGES=TEST_STORAGES)
class AllowedHostsTest(SimpleTestCase):
    @patch.dict(
        os.environ,
        {
            "WODBY": "true",
            "WODBY_HOSTS": '["app.example.com"]',
            "WODBY_APP_SERVICE_NAME": "django",
        },
        clear=True,
    )
    def test_wodby_hosts_include_loopback_probe_targets(self):
        allowed_hosts = get_allowed_hosts(debug=False)

        self.assertEqual(
            allowed_hosts,
            ["app.example.com", "django", "localhost", "127.0.0.1", "[::1]"],
        )
        with override_settings(ALLOWED_HOSTS=allowed_hosts):
            response = self.client.get(
                reverse("core:index"), HTTP_HOST="localhost:8080"
            )

        self.assertEqual(response.status_code, 200)
