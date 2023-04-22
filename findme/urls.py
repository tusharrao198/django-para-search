from django.urls import path
from findme import views
from findme.views import create_paragraphs, search_paragraphs

urlpatterns = [
    path('paragraphs', create_paragraphs),
    path('search/<str:word>/', search_paragraphs),
]