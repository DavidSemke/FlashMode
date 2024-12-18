from django.urls import path

from .views import StudySessionView

app_name = "study_sessions"
urlpatterns = [
    path(
        "study_sessions/<int:study_session_id>/",
        StudySessionView.as_view(),
        name="study_session",
    ),
]
