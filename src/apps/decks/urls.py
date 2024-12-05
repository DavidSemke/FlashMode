from django.urls import path

from .views.deck_detail import DeckDetailView
from .views.deck_list import DeckListView

app_name = "decks"
urlpatterns = [
    path("", DeckListView.as_view(), name="deck_list"),
    path("<int:pk>/", DeckDetailView.as_view(), name="deck_detail"),
]
