from django.conf import settings
from django.forms import ModelForm
from django.test import TestCase
from django.urls import reverse, reverse_lazy

from ....core.model_factories import UserFactory
from ...model_factories import DeckFactory
from ...models import Deck


class DeckCreateViewTest(TestCase):
    url = reverse_lazy("decks:deck_create")

    def setUp(self):
        self.user1 = UserFactory()
        return super().setUp()

    def test_get_guest(self):
        res = self.client.get(self.url)
        # Should redirect to login page
        self.assertEqual(res.status_code, 302)
        self.assertIn(settings.LOGIN_URL, res["Location"])

    def test_get_login(self):
        logged_in = self.client.login(username=self.user1.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        with self.assertTemplateUsed("decks/deck_form.html"):
            res = self.client.get(self.url)
            self.assertEqual(res.status_code, 200)
            self.assertIn("head_title", res.context)
            self.assertIn("main_h1", res.context)
            self.assertIn("is_create_view", res.context)
            self.assertIn("form", res.context)
            self.assertIsInstance(res.context["form"], ModelForm)

    def test_post_guest(self):
        res = self.client.post(self.url, {"title": "title", "private": False})
        self.assertEqual(res.status_code, 302)
        self.assertIn(settings.LOGIN_URL, res["Location"])

    def test_post_login(self):
        logged_in = self.client.login(username=self.user1.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        res = self.client.post(self.url, {"title": "title", "private": False})
        self.assertEqual(res.status_code, 302)
        # User should automatically be added to users M:M relationship on deck create
        self.assertTrue(
            Deck.objects.filter(title="title", users=self.user1.id).exists()
        )


class DeckUpdateViewTest(TestCase):
    def setUp(self):
        self.user1 = UserFactory()
        self.deck1 = DeckFactory(creator=self.user1)
        self.url = reverse("decks:deck_update", kwargs={"deck_id": self.deck1.id})
        return super().setUp()

    def test_get_guest(self):
        res = self.client.get(self.url)
        # Should redirect to login page
        self.assertEqual(res.status_code, 302)
        self.assertIn(settings.LOGIN_URL, res["Location"])

    def test_get_login_not_deck_creator(self):
        user2 = UserFactory()
        logged_in = self.client.login(username=user2.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        with self.assertLogs("django.request", level="WARNING"):
            res = self.client.get(self.url)
            self.assertEqual(res.status_code, 403)

    def test_get_login_deck_creator(self):
        logged_in = self.client.login(username=self.user1.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        with self.assertTemplateUsed("decks/deck_form.html"):
            res = self.client.get(self.url)
            self.assertEqual(res.status_code, 200)
            self.assertIn("head_title", res.context)
            self.assertIn("main_h1", res.context)
            self.assertIn("form", res.context)
            self.assertIsInstance(res.context["form"], ModelForm)

    def test_post_guest(self):
        res = self.client.post(self.url, {"title": "title", "private": False})
        self.assertEqual(res.status_code, 302)
        self.assertIn(settings.LOGIN_URL, res["Location"])

    def test_post_login_not_deck_creator(self):
        user2 = UserFactory()
        logged_in = self.client.login(username=user2.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        with self.assertLogs("django.request", level="WARNING"):
            res = self.client.post(self.url, {"title": "title", "private": False})
            self.assertEqual(res.status_code, 403)

    def test_post_login_deck_creator(self):
        logged_in = self.client.login(username=self.user1.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        # Change the last char of the title
        # Title will not be empty or include special chars
        new_title = self.deck1.title[:-1] + chr(ord(self.deck1.title[-1]) + 1)

        res = self.client.post(self.url, {"title": new_title, "private": False})
        self.assertEqual(res.status_code, 302)

        deck2 = Deck.objects.get(title=new_title)
        self.assertEqual(self.deck1.id, deck2.id)


class DeckDeleteViewTest(TestCase):
    def setUp(self):
        self.user1 = UserFactory()
        self.deck1 = DeckFactory(creator=self.user1)
        self.url = reverse("decks:deck_delete", kwargs={"deck_id": self.deck1.id})
        return super().setUp()

    def test_get_guest(self):
        res = self.client.get(self.url)
        # Should redirect to login page
        self.assertEqual(res.status_code, 302)
        self.assertIn(settings.LOGIN_URL, res["Location"])

    def test_get_login_not_deck_creator(self):
        user2 = UserFactory()
        logged_in = self.client.login(username=user2.username, password="password")
        self.assertTrue(logged_in, "Login failed")
        with self.assertLogs("django.request", level="WARNING"):
            res = self.client.post(self.url)
            self.assertEqual(res.status_code, 403)

    def test_get_login_deck_creator(self):
        logged_in = self.client.login(username=self.user1.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        with self.assertTemplateUsed("decks/deck_confirm_delete.html"):
            res = self.client.get(self.url)
            self.assertEqual(res.status_code, 200)
            self.assertIn("head_title", res.context)
            self.assertIn("main_h1", res.context)

    def test_post_guest(self):
        res = self.client.get(self.url)
        # Should redirect to login page
        self.assertEqual(res.status_code, 302)
        self.assertIn(settings.LOGIN_URL, res["Location"])

    def test_post_login_not_deck_creator(self):
        user2 = UserFactory()
        logged_in = self.client.login(username=user2.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        with self.assertLogs("django.request", level="WARNING"):
            res = self.client.post(self.url)
            self.assertEqual(res.status_code, 403)

    def test_post_login_deck_creator(self):
        logged_in = self.client.login(username=self.user1.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        res = self.client.post(self.url)
        self.assertEqual(res.status_code, 302)

        with self.assertRaises(Deck.DoesNotExist):
            Deck.objects.get(id=self.deck1.id)
