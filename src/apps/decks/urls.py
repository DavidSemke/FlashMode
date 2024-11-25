from django.urls import path

from .views import DeckDetailView, DeckListView

app_name = "decks"
urlpatterns = [
    path("", DeckListView.as_view(), name="deck_list"),
    path("<int:pk>/", DeckDetailView.as_view(), name="deck_detail"),
]
