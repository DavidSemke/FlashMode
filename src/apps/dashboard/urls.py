from django.urls import path

from .views import IndexView, WeeklyGoalUpdateView

app_name = "dashboard"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path(
        "weekly_goal_update/", WeeklyGoalUpdateView.as_view(), name="weekly_goal_update"
    ),
]
