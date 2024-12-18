from django.contrib.auth import get_user_model
from factory import Faker, Iterator, post_generation
from factory.django import DjangoModelFactory

from .models import Card, Deck

User = get_user_model()


class DeckFactory(DjangoModelFactory):
    class Meta:
        model = Deck

    @post_generation
    def users(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        # Add the iterable of users using bulk addition
        self.users.add(*extracted)

    creator = Iterator(User.objects.all())
    create_date = Faker("date")
    title = Faker("text", max_nb_chars=50)
    private = False


class CardFactory(DjangoModelFactory):
    class Meta:
        model = Card

    deck = Iterator(Deck.objects.all())
    question = Faker("text", max_nb_chars=300)
    answer = Faker("text", max_nb_chars=300)
