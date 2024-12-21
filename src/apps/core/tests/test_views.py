from django.test import SimpleTestCase
from django.urls import reverse


class IndexViewTest(SimpleTestCase):
    def test_get(self):
        with self.assertTemplateUsed("core/index.html"):
            res = self.client.get(reverse("core:index"))
            self.assertEqual(res.status_code, 200)
            self.assertIn("head_title", res.context)
