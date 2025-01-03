from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    streak = models.SmallIntegerField()
    weekly_card_count_goal = models.SmallIntegerField()
