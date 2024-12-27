from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from ...core.model_factories import UserFactory


class IndexViewTest(TestCase):
    def test_get_guest(self):
        res = self.client.get(reverse("dashboard:index"))
        # Should redirect to login page
        self.assertEqual(res.status_code, 302)
        self.assertIn(settings.LOGIN_URL, res["Location"])

    def test_get_login(self):
        with self.assertTemplateUsed("dashboard/index.html"):
            user = UserFactory()
            logged_in = self.client.login(username=user.username, password="password")
            self.assertTrue(logged_in, "Login failed")

            res = self.client.get(reverse("dashboard:index"))
            self.assertEqual(res.status_code, 200)
            self.assertIn("head_title", res.context)
            # assert existence of stat keys when defined
