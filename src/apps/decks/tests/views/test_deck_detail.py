import logging

from django.test import TestCase
from django.urls import reverse

from ....core.model_factories import UserFactory
from ...model_factories import DeckFactory
from ...models import Deck


class DeckDetailViewTest(TestCase):
    def get_url(self, deck_id):
        return reverse("decks:deck_detail", kwargs={"deck_id": deck_id})

    def setUp(self):
        self.user1 = UserFactory()
        self.logger = logging.getLogger("django.request")
        return super().setUp()

    def test_get_guest_public_deck(self):
        deck = DeckFactory(creator=self.user1)

        with self.assertTemplateUsed("decks/deck_detail.html"):
            res = self.client.get(self.get_url(deck.id))
            self.assertEqual(res.status_code, 200)
            self.assertIn("head_title", res.context)
            self.assertIn("main_h1", res.context)
            self.assertIn("deck", res.context)

            self.assertIsInstance(res.context["deck"], Deck)

    def test_get_login_private_deck_creator(self):
        deck = DeckFactory(creator=self.user1, private=True)

        # Log in creator of the private deck
        logged_in = self.client.login(username=self.user1.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        res = self.client.get(self.get_url(deck.id))
        self.assertEqual(res.status_code, 200)

    def test_get_guest_private_deck(self):
        deck = DeckFactory(creator=self.user1, private=True)

        with self.assertLogs("django.request", level="WARNING"):
            res = self.client.get(self.get_url(deck.id))
            self.assertEqual(res.status_code, 403)

    def test_get_login_private_deck(self):
        deck = DeckFactory(creator=self.user1, private=True)
        user2 = UserFactory()

        # Log in user that did NOT create private deck
        logged_in = self.client.login(username=user2.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        with self.assertLogs("django.request", level="WARNING"):
            res = self.client.get(self.get_url(deck.id))
            self.assertEqual(res.status_code, 403)
