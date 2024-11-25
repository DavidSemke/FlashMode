from factory import Faker
from factory.django import DjangoModelFactory

from .models import Profile

fake = Faker()


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile
