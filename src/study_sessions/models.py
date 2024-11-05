from django.contrib.auth.models import User
from django.db import models

from decks.models import Card


class StudySession(models.Model):
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="study_sessions"
    )
    create_date = models.DateField(auto_now_add=True)


class Response(models.Model):
    study_session = models.ForeignKey(
        StudySession, on_delete=models.CASCADE, related_name="responses"
    )
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="responses")
    is_correct = models.BooleanField()
