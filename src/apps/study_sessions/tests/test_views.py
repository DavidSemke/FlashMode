from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from ...core.model_factories import UserFactory
from ...decks.model_factories import CardFactory, DeckFactory
from ...decks.models import Deck
from ..model_factories import ResponseFactory, StudySessionFactory
from ..models import Response, StudySession


class StudySessionViewTest(TestCase):
    def get_url(self, ss_id):
        return reverse(
            "study_sessions:study_session", kwargs={"study_session_id": ss_id}
        )

    def setUp(self):
        self.user1 = UserFactory()
        self.deck1 = DeckFactory(creator=self.user1)
        self.study_session1 = StudySessionFactory(student=self.user1, deck=self.deck1)
        self.url = reverse(
            "study_sessions:study_session",
            kwargs={"study_session_id": self.study_session1.id},
        )

    def test_get_guest(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 302)
        self.assertIn(settings.LOGIN_URL, res["Location"])

    def test_get_login_not_study_session_creator(self):
        user2 = UserFactory()
        logged_in = self.client.login(username=user2.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        with self.assertLogs("django.request", level="WARNING"):
            res = self.client.get(self.url)
            self.assertEqual(res.status_code, 403)

    def test_get_login_study_session_creator(self):
        logged_in = self.client.login(username=self.user1.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 200)
        self.assertIn("head_title", res.context)
        self.assertIn("main_h1", res.context)
        self.assertIn("deck_id", res.context)
        self.assertIn("ss_id", res.context)
        self.assertIn("card_list", res.context)
        self.assertIn("card_count", res.context)
        self.assertIn("correct_count", res.context)

    def test_get_login_deck_deleted_study_session_creator(self):
        Deck.objects.get(id=self.deck1.id).delete()

        logged_in = self.client.login(username=self.user1.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        with self.assertLogs("django.request", level="WARNING"):
            res = self.client.get(self.url)
            self.assertEqual(res.status_code, 404)

    def test_get_login_study_session_expired_study_session_creator(self):
        StudySession.objects.filter(id=self.study_session1.id).update(
            create_date=timezone.now() - timezone.timedelta(hours=24)
        )

        logged_in = self.client.login(username=self.user1.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        with self.assertLogs("django.request", level="WARNING"):
            res = self.client.get(self.url)
            self.assertEqual(res.status_code, 410)


class ResponseViewTest(TestCase):
    def setUp(self):
        self.user1 = UserFactory()
        self.deck1 = DeckFactory(creator=self.user1)
        self.card1 = CardFactory(deck=self.deck1)
        self.card2 = CardFactory(deck=self.deck1)
        self.study_session1 = StudySessionFactory(student=self.user1, deck=self.deck1)
        self.url = reverse(
            "study_sessions:response",
            kwargs={"study_session_id": self.study_session1.id},
        )

    def test_get_login(self):
        logged_in = self.client.login(username=self.user1.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        with self.assertLogs("django.request", level="WARNING"):
            res = self.client.get(self.url)
            self.assertEqual(res.status_code, 405)

    def test_post_guest(self):
        res = self.client.post(self.url, {"response_type": "success"})
        self.assertEqual(res.status_code, 302)
        self.assertIn(settings.LOGIN_URL, res["Location"])

    def test_post_login_not_study_session_creator(self):
        user2 = UserFactory()
        logged_in = self.client.login(username=user2.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        with self.assertLogs("django.request", level="WARNING"):
            res = self.client.post(self.url, {"response_type": "success"})
            self.assertEqual(res.status_code, 403)

    def test_post_login_study_session_creator(self):
        ResponseFactory(
            study_session=self.study_session1,
            card=self.card1,
            position=1,
            is_correct=None,
        )
        ResponseFactory(
            study_session=self.study_session1,
            card=self.card2,
            position=2,
            is_correct=None,
        )

        logged_in = self.client.login(username=self.user1.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        res = self.client.post(self.url, {"response_type": "success"})
        self.assertEqual(res.status_code, 204)
        response = Response.objects.order_by("position")[0]
        self.assertTrue(response.is_correct)

        res = self.client.post(self.url, {"response_type": "error"})
        self.assertEqual(res.status_code, 204)
        response = Response.objects.order_by("position")[1]
        self.assertFalse(response.is_correct)

    def test_post_login_deck_deleted_study_session_creator(self):
        Deck.objects.get(id=self.deck1.id).delete()

        logged_in = self.client.login(username=self.user1.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        with self.assertLogs("django.request", level="WARNING"):
            res = self.client.post(self.url, {"response_type": "success"})
            self.assertEqual(res.status_code, 404)

    def test_post_login_study_session_expired_study_session_creator(self):
        StudySession.objects.filter(id=self.study_session1.id).update(
            create_date=timezone.now() - timezone.timedelta(hours=24)
        )

        logged_in = self.client.login(username=self.user1.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        with self.assertLogs("django.request", level="WARNING"):
            res = self.client.post(self.url, {"response_type": "success"})
            self.assertEqual(res.status_code, 410)

    def test_post_login_study_session_creator_no_more_responses(self):
        logged_in = self.client.login(username=self.user1.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        with self.assertLogs("django.request", level="WARNING"):
            res = self.client.post(self.url, {"response_type": "success"})
            self.assertEqual(res.status_code, 404)

    def test_post_login_study_session_creator_invalid_response_type(self):
        ResponseFactory(
            study_session=self.study_session1,
            card=self.card1,
            position=1,
            is_correct=None,
        )

        logged_in = self.client.login(username=self.user1.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        with self.assertLogs("django.request", level="WARNING"):
            res = self.client.post(self.url, {"response_type": ""})
            self.assertEqual(res.status_code, 400)
