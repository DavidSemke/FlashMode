import logging

from django.test import TestCase
from django.urls import reverse

from ....core.model_factories import UserFactory
from ....study_sessions.models import Response, StudySession
from ...model_factories import DeckFactory
from ...models import Card, Deck


class DeckPlayViewTest(TestCase):
    def setUp(self):
        self.user1 = UserFactory()
        self.deck1 = DeckFactory(creator=self.user1)
        self.card1 = Card(deck=self.deck1)
        self.url = reverse("decks:deck_play", kwargs={"deck_id": self.deck1.id})
        self.logger = logging.getLogger("django.request")
        return super().setUp()

    def test_get_guest_public_deck(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 302)

        # There will only be no study sessions since user is guest
        study_sessions = StudySession.objects.all()
        self.assertEqual(len(study_sessions), 0)

    def test_get_login_public_deck(self):
        user2 = UserFactory()
        logged_in = self.client.login(username=user2.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 302)

        # There will only be one study session
        study_sessions = StudySession.objects.all()
        self.assertEqual(len(study_sessions), 1)
        ss = study_sessions[0]

        # Response for each card in deck
        card_count = Card.objects.filter(deck=self.deck1).count()
        response_count = Response.objects.filter(study_session=ss).count()
        self.assertEqual(card_count, response_count)

    def test_get_guest_private_deck(self):
        Deck.objects.filter(id=self.deck1.id).update(private=True)

        with self.assertLogs("django.request", level="WARNING"):
            res = self.client.get(self.url)
            self.assertEqual(res.status_code, 403)

    def test_get_login_not_private_deck_creator(self):
        Deck.objects.filter(id=self.deck1.id).update(private=True)

        user2 = UserFactory()
        logged_in = self.client.login(username=user2.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        with self.assertLogs("django.request", level="WARNING"):
            res = self.client.get(self.url)
            self.assertEqual(res.status_code, 403)

    def test_get_login_private_deck_creator(self):
        Deck.objects.filter(id=self.deck1.id).update(private=True)

        logged_in = self.client.login(username=self.user1.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 302)

        # There will only be one study session
        study_sessions = StudySession.objects.all()
        self.assertEqual(len(study_sessions), 1)
        ss = study_sessions[0]

        # Response for each card in deck
        card_count = Card.objects.filter(deck=self.deck1).count()
        response_count = Response.objects.filter(study_session=ss).count()
        self.assertEqual(card_count, response_count)
