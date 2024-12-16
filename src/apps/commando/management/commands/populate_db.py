from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from ....core.model_factories import UserFactory
from ....decks.model_factories import (
    CardFactory,
    DeckFactory,
    ResponseFactory,
    StudySessionFactory,
)
from ....decks.models import Card, Deck, Response, StudySession


class Command(BaseCommand):
    help = "Insert placeholder data into the database."

    def handle(self, *args, **kwargs):
        self._clear_tables()

        users = self._insert_users()

        deck_count = 10
        self._insert_decks(users, deck_count)

        card_count = deck_count * 10
        self._insert_cards(card_count)

        study_session_count = len(users) * 10
        self._insert_study_sessions(study_session_count)

        response_count = study_session_count * 10
        self._insert_responses(response_count)

    def _clear_tables(self):
        User = get_user_model()
        # Exclude super-user, test-user
        User.objects.exclude(id__in=[8, 9]).delete()

        for model in (Deck, Card, StudySession, Response):
            model.objects.all().delete()

    # Handles 1-1 relationships (e.g. Profile)
    def _insert_users(self, count=3):
        self.stdout.write("Inserting users...")
        return [UserFactory() for _ in range(count)]

    def _insert_decks(self, users, count=10):
        self.stdout.write("Inserting decks...")
        return [DeckFactory(users=users) for _ in range(count)]

    def _insert_cards(self, count):
        self.stdout.write("Inserting cards...")
        return [CardFactory() for _ in range(count)]

    def _insert_study_sessions(self, count):
        self.stdout.write("Inserting study sessions...")
        return [StudySessionFactory() for _ in range(count)]

    def _insert_responses(self, count):
        self.stdout.write("Inserting responses...")
        return [ResponseFactory() for _ in range(count)]
