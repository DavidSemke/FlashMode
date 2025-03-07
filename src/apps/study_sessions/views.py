from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import TemplateView, View

from .models import Response, StudySession


class StudySessionView(LoginRequiredMixin, TemplateView):
    template_name = "study_sessions/study_session.html"

    def get(self, request, *args, **kwargs):
        ss_id = kwargs.get("study_session_id")
        self.study_session = get_object_or_404(
            StudySession.objects.select_related("deck"), id=ss_id
        )
        self.deck = self.study_session.deck

        if self.study_session.student.id != request.user.id:
            raise PermissionDenied("Study session was not created by current user.")

        if self.deck is None:
            raise Http404("Deck of study session does not exist.")

        if self.study_session.create_date <= timezone.now() - timezone.timedelta(
            hours=24
        ):
            return HttpResponse(content="This study session has expired.", status=410)

        # Each response corresponds to one card in the study session's deck
        # If a card is deleted, response is useless unless is_correct is set
        Response.objects.filter(
            study_session=ss_id, card__isnull=True, is_correct__isnull=True
        ).delete()

        responses = list(
            Response.objects.select_related("card")
            .filter(study_session=ss_id)
            .order_by("position")
        )

        if len(responses) == 0:
            return HttpResponse(
                content="All cards from this deck have been deleted.", status=422
            )

        correct_responses = []
        self.cards = []

        for res in responses:
            if res.is_correct is None:
                self.cards.append(
                    {
                        "id": res.card.id,
                        "question": res.card.question,
                        "answer": res.card.answer,
                    }
                )
            elif res.is_correct is True:
                correct_responses.append(res)

        self.card_count = len(responses)
        self.correct_count = len(correct_responses)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["deck_id"] = self.deck.id
        context["ss_id"] = self.study_session.id
        context["card_list"] = self.cards
        context["card_count"] = self.card_count
        context["correct_count"] = self.correct_count
        context["main_h1"] = f"Study Session - Deck '{self.deck.title}'"
        context["head_title"] = f"{context['main_h1']} - FlashMode"
        return context


class ResponseView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        study_session = get_object_or_404(
            StudySession.objects.select_related("student").select_related("deck"),
            id=kwargs.get("study_session_id"),
        )

        if study_session.student.id != request.user.id:
            raise PermissionDenied("Study session was not created by current user.")

        if study_session.deck is None:
            raise Http404("Deck of study session does not exist.")

        if study_session.create_date <= timezone.now() - timezone.timedelta(hours=24):
            return HttpResponse(content="This study session has expired.", status=410)

        next_response = (
            Response.objects.filter(
                study_session=study_session,
                is_correct__isnull=True,
            )
            .order_by("position")
            .first()
        )

        if next_response is None:
            raise Http404("Study session has no more responses.")

        response_type = request.POST.get("response_type")

        if response_type == "error":
            is_correct = False
        elif response_type == "success":
            is_correct = True
        else:
            return HttpResponseBadRequest(
                "Value of key 'response_type' in request body must be in"
                + " ['error', 'success']."
            )

        next_response.is_correct = is_correct
        next_response.save()

        return HttpResponse(status=204)
