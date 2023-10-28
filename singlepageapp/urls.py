from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("generate", views.process_text, name="generate")
]