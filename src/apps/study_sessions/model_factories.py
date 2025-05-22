from django.contrib.auth import get_user_model
from factory import Faker, Iterator, LazyAttribute
from factory.django import DjangoModelFactory

from ..decks.models import Card, Deck
from .models import Response, StudySession

User = get_user_model()


class StudySessionFactory(DjangoModelFactory):
    class Meta:
        model = StudySession

    student = Iterator(User.objects.all())
    deck = Iterator(Deck.objects.all())


class ResponseFactory(DjangoModelFactory):
    class Meta:
        model = Response

    class Params:
        is_correct_bool = Faker("pybool")

    study_session = Iterator(StudySession.objects.all())
    card = LazyAttribute(
        lambda obj: Card.objects.filter(deck=obj.study_session.deck)
        .exclude(
            pk__in=Response.objects.filter(study_session=obj.study_session).values_list(
                "card__pk", flat=True
            )
        )
        .first()
    )
    position = LazyAttribute(
        lambda obj: (
            max(
                Response.objects.filter(study_session=obj.study_session).values_list(
                    "position", flat=True
                ),
                default=0,
            )
            + 1
        )
    )
    is_correct = LazyAttribute(
        lambda obj: None
        if Response.objects.filter(
            study_session=obj.study_session,
            position__lt=obj.position,
            is_correct=None,
        ).exists()
        else obj.is_correct_bool
    )
