from django.conf import settings
from django.forms import ModelForm
from django.test import TestCase
from django.urls import reverse

from ....core.model_factories import UserFactory
from ...model_factories import CardFactory, DeckFactory
from ...models import Card


# Whether or not a deck is private does not matter here.
# If a user did not create the deck, access is denied.
class CardCreateViewTest(TestCase):
    def setUp(self):
        self.user1 = UserFactory()
        deck = DeckFactory(creator=self.user1)
        self.url = reverse("decks:card_create", kwargs={"deck_id": deck.id})
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

        with self.assertTemplateUsed("decks/card_form.html"):
            res = self.client.get(self.url)
            self.assertEqual(res.status_code, 200)
            self.assertIn("head_title", res.context)
            self.assertIn("main_h1", res.context)
            self.assertIn("deck", res.context)
            self.assertIn("form", res.context)
            self.assertIsInstance(res.context["form"], ModelForm)

    def test_post_guest(self):
        res = self.client.post(self.url, {"question": "1", "answer": "2"})
        self.assertEqual(res.status_code, 302)
        self.assertIn(settings.LOGIN_URL, res["Location"])

    def test_post_login_not_deck_creator(self):
        user2 = UserFactory()
        logged_in = self.client.login(username=user2.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        with self.assertLogs("django.request", level="WARNING"):
            res = self.client.post(self.url, {"question": "1", "answer": "2"})
            self.assertEqual(res.status_code, 403)

    def test_post_login_deck_creator(self):
        logged_in = self.client.login(username=self.user1.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        res = self.client.post(self.url, {"question": "1", "answer": "2"})
        self.assertEqual(res.status_code, 302)
        self.assertTrue(Card.objects.filter(question="1", answer="2").exists())


class CardUpdateViewTest(TestCase):
    def setUp(self):
        self.user1 = UserFactory()
        deck = DeckFactory(creator=self.user1)
        self.card1 = CardFactory(deck=deck)
        self.url = reverse(
            "decks:card_update", kwargs={"deck_id": deck.id, "card_id": self.card1.id}
        )
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

        with self.assertTemplateUsed("decks/card_form.html"):
            res = self.client.get(self.url)
            self.assertEqual(res.status_code, 200)
            self.assertIn("head_title", res.context)
            self.assertIn("main_h1", res.context)
            self.assertIn("deck", res.context)
            self.assertIn("form", res.context)
            self.assertIsInstance(res.context["form"], ModelForm)

    def test_post_guest(self):
        res = self.client.post(self.url, {"question": "1", "answer": "2"})
        self.assertEqual(res.status_code, 302)
        self.assertIn(settings.LOGIN_URL, res["Location"])

    def test_post_login_not_deck_creator(self):
        user2 = UserFactory()
        logged_in = self.client.login(username=user2.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        with self.assertLogs("django.request", level="WARNING"):
            res = self.client.post(self.url, {"question": "1", "answer": "2"})
            self.assertEqual(res.status_code, 403)

    def test_post_login_deck_creator(self):
        logged_in = self.client.login(username=self.user1.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        # Change the last char of the question
        # Title will not be empty or include special chars
        question = self.card1.question[:-1] + chr(ord(self.card1.question[-1]) + 1)
        res = self.client.post(
            self.url, {"question": question, "answer": self.card1.answer}
        )
        self.assertEqual(res.status_code, 302)

        card2 = Card.objects.get(question=question)
        self.assertEqual(self.card1.id, card2.id)


class CardDeleteViewTest(TestCase):
    def setUp(self):
        self.user1 = UserFactory()
        deck = DeckFactory(creator=self.user1)
        self.card1 = CardFactory(deck=deck)
        self.url = reverse(
            "decks:card_delete", kwargs={"deck_id": deck.id, "card_id": self.card1.id}
        )
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

        with self.assertTemplateUsed("decks/card_confirm_delete.html"):
            res = self.client.get(self.url)
            self.assertEqual(res.status_code, 200)
            self.assertIn("head_title", res.context)
            self.assertIn("main_h1", res.context)
            self.assertIn("deck", res.context)

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

        self.assertFalse(Card.objects.filter(id=self.card1.id).exists())
