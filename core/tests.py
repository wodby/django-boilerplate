from django.test import SimpleTestCase, override_settings
from django.urls import reverse

from core.tasks import add


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        },
    }
)
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
