from django.conf import settings
from django.test import TestCase
from django.urls import reverse_lazy

from ....core.model_factories import UserFactory
from ...model_factories import DeckFactory
from ...models import Deck


class DeckListViewTest(TestCase):
    url = reverse_lazy("decks:deck_list")

    def setUp(self):
        self.user1 = UserFactory()
        self.user2 = UserFactory()

        DeckFactory(creator=self.user1, title="I am a title 1")
        DeckFactory(creator=self.user1, title="I am a title 2", private=True)
        DeckFactory(creator=self.user2, title="I am a title 3")

        return super().setUp()

    def test_get(self):
        with self.assertTemplateUsed("decks/deck_list.html"):
            res = self.client.get(self.url)
            self.assertEqual(res.status_code, 200)
            self.assertIn("head_title", res.context)
            self.assertIn("main_h1", res.context)
            self.assertIn("deck_list", res.context)

            deck_list = res.context["deck_list"]

            for deck in deck_list:
                self.assertIsInstance(deck, Deck)

            # User is anonymous, so only private deck is hidden
            self.assertEqual(len(deck_list), 2)

    def test_get_login_private_creator(self):
        # Log in creator of the private deck
        logged_in = self.client.login(username=self.user1.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        res = self.client.get(self.url)
        self.assertEqual(res.status_code, 200)

        deck_list = res.context["deck_list"]
        self.assertEqual(len(deck_list), 3)

    def test_get_search_query_param(self):
        res = self.client.get(self.url, query_params={"search": "1"})
        self.assertEqual(res.status_code, 200)

        deck_list = res.context["deck_list"]
        self.assertEqual(len(deck_list), 1)

        res = self.client.get(self.url, query_params={"search": "title"})
        self.assertEqual(res.status_code, 200)

        deck_list = res.context["deck_list"]
        self.assertEqual(len(deck_list), 2)

    def test_get_creator_id_query_param(self):
        res = self.client.get(self.url, query_params={"creator_id": self.user1.id})
        self.assertEqual(res.status_code, 200)

        deck_list = res.context["deck_list"]
        self.assertEqual(len(deck_list), 1)
        self.assertEqual(deck_list[0].creator.id, self.user1.id)

    def test_get_guest_collected_query_param(self):
        # Param collected only applied when logged in
        # Expect redirect to login page
        res = self.client.get(self.url, query_params={"collected": "true"})
        self.assertEqual(res.status_code, 302)
        self.assertIn(settings.LOGIN_URL, res["Location"])

    # Collected decks result in quick deck access for user
    def test_get_login_collected_query_param(self):
        logged_in = self.client.login(username=self.user1.username, password="password")
        self.assertTrue(logged_in, "Login failed")

        # Decks created by user have not been collected
        res = self.client.get(self.url, query_params={"collected": "true"})
        self.assertEqual(res.status_code, 200)
        deck_list = res.context["deck_list"]
        self.assertEqual(len(deck_list), 0)

        # Make user collect private deck made by them
        deck1 = Deck.objects.get(title="I am a title 2", private=True)
        deck1.users.add(self.user1)
        # List the one collected deck
        res = self.client.get(self.url, query_params={"collected": "true"})
        self.assertEqual(res.status_code, 200)
        deck_list = res.context["deck_list"]
        self.assertEqual(len(deck_list), 1)

        # List all decks NOT collected by user
        res = self.client.get(self.url, query_params={"collected": "false"})
        self.assertEqual(res.status_code, 200)
        deck_list = res.context["deck_list"]
        self.assertEqual(len(deck_list), 2)

        # Make user collect deck not made by them
        foreign_deck = Deck.objects.get(title="I am a title 3")
        foreign_deck.users.add(self.user1)
        # List all decks collected by user
        res = self.client.get(self.url, query_params={"collected": "true"})
        self.assertEqual(res.status_code, 200)

        deck_list = res.context["deck_list"]
        self.assertEqual(len(deck_list), 2)
