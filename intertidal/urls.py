from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("mockup/<int:version>", views.mockup, name="mockup"),
    path("resources/<int:pk>", views.ResourceDetailsView.as_view(), name="resource-details"),
]