from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class IndexViewTest(TestCase):
    def test_get_no_login(self):
        res = self.client.get(reverse("dashboard:index"))
        # Should redirect to login page
        self.assertEqual(res.status_code, 302)
        self.assertIn(settings.LOGIN_URL, res["Location"])

    def test_get_login(self):
        with self.assertTemplateUsed("dashboard/index.html"):
            password = "noodle"
            user = User.objects.create_user(username="freddie", password=password)
            logged_in = self.client.login(username=user.username, password=password)
            self.assertTrue(logged_in, "Login failed")

            res = self.client.get(reverse("dashboard:index"))
            self.assertEqual(res.status_code, 200)
            self.assertIn("head_title", res.context)
            # assert existence of stat keys when defined
