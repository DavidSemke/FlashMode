from factory import Faker
from factory.django import DjangoModelFactory

from .models import Profile


# Foreign key handled by UserFactory
class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile

    streak = Faker("random_int", min=0, max=999)
    weekly_card_count_goal = Faker("random_int", min=0, max=999)
