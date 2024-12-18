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
    create_date = Faker("date")


class ResponseFactory(DjangoModelFactory):
    class Meta:
        model = Response

    study_session = Iterator(StudySession.objects.all())
    card = LazyAttribute(
        lambda obj: Card.objects.filter(deck=obj.study_session.deck)
        .order_by("?")
        .first()
    )
    is_correct = Faker("pybool")
