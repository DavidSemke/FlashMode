from django.contrib.auth import get_user_model
from factory import Faker, RelatedFactory
from factory.django import DjangoModelFactory

from ..dashboard.model_factories import ProfileFactory

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Faker("name")
    password = "password"
    email = Faker("email")

    profile = RelatedFactory(ProfileFactory, factory_related_name="user")
