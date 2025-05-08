from django.conf import settings
from django.db import models
from django.db.models.signals import post_save


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    streak = models.PositiveSmallIntegerField(default=0)
    weekly_card_count_goal = models.PositiveSmallIntegerField(default=0)


# Use signal to create profile when user created
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()


post_save.connect(create_profile, sender=settings.AUTH_USER_MODEL)
