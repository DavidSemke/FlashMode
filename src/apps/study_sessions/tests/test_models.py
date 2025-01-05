from django.core.exceptions import ValidationError
from django.test import TestCase

from ...core.model_factories import UserFactory
from ...decks.model_factories import CardFactory, DeckFactory
from ..model_factories import ResponseFactory, StudySessionFactory


class ResponseModelTest(TestCase):
    def setUp(self):
        user = UserFactory()
        self.deck1 = DeckFactory(creator=user)
        self.deck2 = DeckFactory(creator=user)

        self.card1 = CardFactory(deck=self.deck1)
        self.card2 = CardFactory(deck=self.deck1)
        self.card3 = CardFactory(deck=self.deck2)

        self.study_session1 = StudySessionFactory(student=user, deck=self.deck1)

    def test_valid_model(self):
        try:
            ResponseFactory(study_session=self.study_session1, card=self.card1)
        except ValidationError as e:
            self.fail(f"Unexpected ValidationError:\n{e}")

    def test_study_session_card_pair_not_unique(self):
        ResponseFactory(study_session=self.study_session1, card=self.card1)

        with self.assertRaises(ValidationError) as cm:
            ResponseFactory(study_session=self.study_session1, card=self.card1)

        error_dict = cm.exception.error_dict
        self.assertIn("__all__", error_dict)
        self.assertIn(
            "Response with this Study session and Card already exists.",
            error_dict["__all__"][0].messages,
        )

    def test_study_session_position_pair_not_unique(self):
        ResponseFactory(study_session=self.study_session1, card=self.card1, position=1)

        with self.assertRaises(ValidationError) as cm:
            ResponseFactory(
                study_session=self.study_session1, card=self.card2, position=1
            )

        error_dict = cm.exception.error_dict
        self.assertIn("__all__", error_dict)
        self.assertIn(
            "Response with this Study session and Position already exists.",
            error_dict["__all__"][0].messages,
        )

    def test_card_deck_is_not_study_session_deck(self):
        with self.assertRaises(ValidationError) as cm:
            ResponseFactory(study_session=self.study_session1, card=self.card3)

        error_dict = cm.exception.error_dict
        self.assertIn("__all__", error_dict)
        self.assertIn(
            "Card deck must match study session deck.",
            error_dict["__all__"][0].messages,
        )

    def test_response_used_before_previous(self):
        ResponseFactory(
            study_session=self.study_session1,
            card=self.card1,
            position=1,
            is_correct=None,
        )

        with self.assertRaises(ValidationError) as cm:
            ResponseFactory(
                study_session=self.study_session1,
                card=self.card2,
                position=2,
                is_correct=True,
            )

        error_dict = cm.exception.error_dict
        self.assertIn("__all__", error_dict)
        self.assertIn(
            "If 'is_correct' is null, all subsequent responses in the same"
            + " study session must also have 'is_correct' as null.",
            error_dict["__all__"][0].messages,
        )
