from django.urls import path
from . import views
from cuboidapp.views import home, about

urlpatterns = [
    path("", views.home, name="home"),
    path("about", views.about, name="about"),
]