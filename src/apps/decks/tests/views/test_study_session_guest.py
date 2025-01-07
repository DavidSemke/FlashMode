import logging

from django.test import TestCase
from django.urls import reverse

from ....core.model_factories import UserFactory
from ...model_factories import DeckFactory
from ...models import Deck


class StudySessionGuestViewTest(TestCase):
    def setUp(self):
        self.user1 = UserFactory()
        self.deck1 = DeckFactory(creator=self.user1)
        self.url = reverse(
            "decks:study_session_guest", kwargs={"deck_id": self.deck1.id}
        )
        self.logger = logging.getLogger("django.request")
        return super().setUp()

    def test_get_guest_public_deck(self):
        with self.assertTemplateUsed("decks/study_session_guest.html"):
            res = self.client.get(self.url)

        self.assertEqual(res.status_code, 200)
        self.assertIn("card_list", res.context)
        self.assertIn("card_count", res.context)
        self.assertIn("main_h1", res.context)
        self.assertIn("head_title", res.context)

    def test_get_login_public_deck(self):
        user2 = UserFactory()
        logged_in = self.client.login(username=user2.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 302)
        self.assertIn(
            reverse("decks:deck_play", kwargs={"deck_id": self.deck1.id}),
            res["Location"],
        )

    def test_get_guest_private_deck(self):
        Deck.objects.filter(id=self.deck1.id).update(private=True)

        with self.assertLogs("django.request", level="WARNING"):
            res = self.client.get(self.url)

        self.assertEqual(res.status_code, 403)

    def test_get_login_private_deck_not_deck_creator(self):
        Deck.objects.filter(id=self.deck1.id).update(private=True)

        user2 = UserFactory()
        logged_in = self.client.login(username=user2.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 302)
        self.assertIn(
            reverse("decks:deck_play", kwargs={"deck_id": self.deck1.id}),
            res["Location"],
        )

    def test_get_login_private_deck_deck_creator(self):
        Deck.objects.filter(id=self.deck1.id).update(private=True)

        logged_in = self.client.login(username=self.user1.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 302)
        self.assertIn(
            reverse("decks:deck_play", kwargs={"deck_id": self.deck1.id}),
            res["Location"],
        )
