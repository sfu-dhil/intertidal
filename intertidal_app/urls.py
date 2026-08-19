from django.urls import include, path

from . import views
from .api import router

urlpatterns = [
    path('', views.home, name='home'),
    path('resources/<int:pk>', views.ResourceDetailsView.as_view(), name='resource-details'),
    path('api/', include(router.urls)),
]