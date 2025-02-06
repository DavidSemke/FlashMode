from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from ....core.model_factories import UserFactory
from ...model_factories import CardFactory, DeckFactory
from ...models import Card


# Whether or not a deck is private does not matter here.
# If a user did not create the deck, access is denied.
class CardListViewTest(TestCase):
    def setUp(self):
        self.user1 = UserFactory()
        self.deck = DeckFactory(creator=self.user1)
        self.url = reverse("decks:card_list", kwargs={"deck_id": self.deck.id})
        return super().setUp()

    def test_get_guest(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 302)
        self.assertIn(settings.LOGIN_URL, res["Location"])

    def test_get_login_not_deck_creator(self):
        user2 = UserFactory()

        # Log in user that did NOT create private deck
        logged_in = self.client.login(username=user2.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        # Already logged in, so expect 403
        with self.assertLogs("django.request", level="WARNING"):
            res = self.client.get(self.url)
            self.assertEqual(res.status_code, 403)

    def test_get_login_deck_creator(self):
        CardFactory(deck=self.deck)

        # Log in creator of the deck
        logged_in = self.client.login(username=self.user1.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        with self.assertTemplateUsed("decks/card_list.html"):
            res = self.client.get(self.url)
            self.assertEqual(res.status_code, 200)
            self.assertIn("head_title", res.context)
            self.assertIn("main_h1", res.context)
            self.assertIn("deck", res.context)
            self.assertIn("card_list", res.context)

            card_list = res.context["card_list"]

            for card in card_list:
                self.assertIsInstance(card, Card)

            self.assertEqual(len(card_list), 1)
