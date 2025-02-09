from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from ....core.model_factories import UserFactory
from ...model_factories import DeckFactory
from ...models import Deck


class DeckCollectViewTest(TestCase):
    def get_url(self, deck_id):
        return reverse("decks:deck_collect", kwargs={"deck_id": deck_id})

    def setUp(self):
        self.user1 = UserFactory()
        return super().setUp()

    def test_get_login(self):
        deck = DeckFactory(creator=self.user1)

        logged_in = self.client.login(username=self.user1.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        with self.assertLogs("django.request", level="WARNING"):
            res = self.client.get(self.get_url(deck.id))
            self.assertEqual(res.status_code, 405)

    def test_post_guest(self):
        deck = DeckFactory(creator=self.user1)

        res = self.client.post(self.get_url(deck.id))
        self.assertEqual(res.status_code, 302)
        self.assertIn(settings.LOGIN_URL, res["Location"])

    def test_post_login_public_deck_uncollect(self):
        deck = DeckFactory(creator=self.user1, users=[self.user1])
        # user1 has collected the deck
        self.assertTrue(Deck.objects.filter(id=deck.id, users=self.user1.id).exists())

        logged_in = self.client.login(username=self.user1.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        res = self.client.post(self.get_url(deck.id))
        self.assertEqual(res.status_code, 302)
        self.assertIn(
            reverse("decks:deck_detail", kwargs={"deck_id": deck.id}), res["Location"]
        )

        # Deck should no longer reference user1 in M to M relationship (uncollected)
        self.assertFalse(Deck.objects.filter(id=deck.id, users=self.user1.id).exists())

    def test_post_login_public_deck_collect(self):
        deck = DeckFactory(creator=self.user1)
        # user2 does not collect deck
        user2 = UserFactory()

        logged_in = self.client.login(username=user2.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        res = self.client.post(self.get_url(deck.id))
        self.assertEqual(res.status_code, 302)
        self.assertIn(
            reverse("decks:deck_detail", kwargs={"deck_id": deck.id}), res["Location"]
        )

        # Deck should now reference user2 in M to M relationship (collected)
        self.assertTrue(Deck.objects.filter(id=deck.id, users=user2.id).exists())

    def test_post_login_private_deck_creator(self):
        deck = DeckFactory(creator=self.user1, private=True)

        logged_in = self.client.login(username=self.user1.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        res = self.client.post(self.get_url(deck.id))
        self.assertEqual(res.status_code, 302)
        self.assertIn(
            reverse("decks:deck_detail", kwargs={"deck_id": deck.id}), res["Location"]
        )

    def test_post_login_not_private_deck_creator(self):
        deck = DeckFactory(creator=self.user1, private=True)
        user2 = UserFactory()

        # Log in user that did NOT create private deck
        logged_in = self.client.login(username=user2.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        with self.assertLogs("django.request", level="WARNING"):
            res = self.client.post(self.get_url(deck.id))
            self.assertEqual(res.status_code, 403)
