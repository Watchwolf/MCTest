from django.urls import path
from . import views

urlpatterns = [
    path("stats/", views.stats, name="copropriete-stats"),
    path("add/", views.add, name="copropriete-add"),
]