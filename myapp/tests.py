from django.test import SimpleTestCase


class ViewsTest(SimpleTestCase):
    def test_index(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"message": "Hello from Wodby Django"})

    def test_healthz(self):
        response = self.client.get("/healthz")

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "ok"})
