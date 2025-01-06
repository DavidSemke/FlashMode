from django.urls import path

from .views import ResponseView, StudySessionView

app_name = "study_sessions"
urlpatterns = [
    path(
        "<int:study_session_id>/",
        StudySessionView.as_view(),
        name="study_session",
    ),
    path(
        "<int:study_session_id>/response",
        ResponseView.as_view(),
        name="response",
    ),
]
