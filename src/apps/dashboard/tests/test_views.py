from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy

from ...core.model_factories import UserFactory

User = get_user_model()


class IndexViewTest(TestCase):
    url = reverse_lazy("dashboard:index")

    def test_get_guest(self):
        res = self.client.get(self.url)
        # Should redirect to login page
        self.assertEqual(res.status_code, 302)
        self.assertIn(settings.LOGIN_URL, res["Location"])

    def test_get_login(self):
        user = UserFactory()

        logged_in = self.client.login(username=user.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        with self.assertTemplateUsed("dashboard/index.html"):
            res = self.client.get(self.url)

        self.assertEqual(res.status_code, 200)
        self.assertIn("weekly_goal", res.context)
        self.assertIn("weekly_goal_progress", res.context)
        self.assertIn("recent_decks", res.context)
        self.assertIn("head_title", res.context)


class WeeklyGoalUpdateViewTest(TestCase):
    url = reverse_lazy("dashboard:weekly_goal_update")

    def test_get_guest(self):
        res = self.client.get(self.url)
        # Should redirect to login page
        self.assertEqual(res.status_code, 302)
        self.assertIn(settings.LOGIN_URL, res["Location"])

    def test_get_login(self):
        user = UserFactory()

        logged_in = self.client.login(username=user.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        with self.assertLogs("django.request", level="WARNING"):
            res = self.client.get(self.url)
            self.assertEqual(res.status_code, 405)

    def test_post_login(self):
        user = UserFactory()
        init_weekly_goal = user.profile.weekly_card_count_goal

        logged_in = self.client.login(username=user.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        new_weekly_goal = 999

        if init_weekly_goal == new_weekly_goal:
            new_weekly_goal -= 1

        res = self.client.post(self.url, {"weekly_goal": str(new_weekly_goal)})
        self.assertEqual(res.status_code, 302)

        updated_user = User.objects.get(id=user.id)

        self.assertTrue(updated_user.profile.weekly_card_count_goal == new_weekly_goal)

    def test_post_login_invalid_weekly_goal_type(self):
        user = UserFactory()

        logged_in = self.client.login(username=user.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        with self.assertLogs("django.request", level="WARNING"):
            res = self.client.post(self.url, {"weekly_goal": ""})
            self.assertEqual(res.status_code, 400)

    def test_post_login_invalid_weekly_goal_value(self):
        user = UserFactory()

        logged_in = self.client.login(username=user.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        with self.assertLogs("django.request", level="WARNING"):
            res = self.client.post(self.url, {"weekly_goal": "1000"})
            self.assertEqual(res.status_code, 400)
