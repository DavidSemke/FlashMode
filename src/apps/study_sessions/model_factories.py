from django.contrib.auth import get_user_model
from factory import Faker, Iterator
from factory.django import DjangoModelFactory

from ..decks.models import Card
from .models import Response, StudySession

User = get_user_model()


class StudySessionFactory(DjangoModelFactory):
    class Meta:
        model = StudySession

    student = Iterator(User.objects.all())
    create_date = Faker("date")


class ResponseFactory(DjangoModelFactory):
    class Meta:
        model = Response

    study_session = Iterator(StudySession.objects.all())
    card = Iterator(Card.objects.all())
    is_correct = Faker("pybool")
