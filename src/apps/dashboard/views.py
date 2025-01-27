from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView, View

from ..dashboard.models import Profile
from ..decks.models import Deck
from ..study_sessions.models import Response


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"

    def get(self, request, *args, **kwargs):
        now = timezone.now()
        # Subtract days to reach Sunday
        days_to_subtract = now.weekday() + 1 if now.weekday() != 6 else 0
        most_recent_sunday = (now - timezone.timedelta(days=days_to_subtract)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )

        week_card_count = Response.objects.filter(
            study_session__create_date__gte=most_recent_sunday,
            study_session__student=request.user.id,
            is_correct__isnull=False,
        ).count()
        profile = Profile.objects.get(id=request.user.id)
        self.weekly_goal = profile.weekly_card_count_goal
        self.weekly_goal_progress = None

        if self.weekly_goal != 0:
            progress_percent = round(week_card_count / self.weekly_goal * 100)
            self.weekly_goal_progress = min(100, progress_percent)

        self.recent_decks = (
            Deck.objects.filter(
                study_sessions__create_date__gte=most_recent_sunday,
                study_sessions__student=request.user.id,
            )
            .annotate(card_count=Count("cards"))
            .distinct()[:5]
        )

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["weekly_goal"] = self.weekly_goal
        context["weekly_goal_progress"] = self.weekly_goal_progress
        context["recent_decks"] = self.recent_decks
        context["head_title"] = "FlashMode - Dashboard"
        return context


class WeeklyGoalUpdateView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        profile = get_object_or_404(
            Profile,
            id=request.user.id,
        )

        weekly_goal = request.POST.get("weekly_goal")

        if not weekly_goal.isdigit():
            return HttpResponseBadRequest(
                "Value of key 'weekly_goal' in request body must be an integer."
            )

        weekly_goal = int(weekly_goal)

        if weekly_goal > 999 or weekly_goal < 0:
            return HttpResponseBadRequest(
                "Value of key 'weekly_goal' in request body must be an integer in range [0, 999]."
            )

        profile.weekly_card_count_goal = weekly_goal
        profile.save()

        return redirect(reverse("dashboard:index"))
