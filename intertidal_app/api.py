from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.conf import settings
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.renderers import JSONRenderer

from .serializers import ResourceSerializer, PersonSerializer, OrganizationSerializer
from .models import Resource, Person, Organization

class CachedReadOnlyModelViewSet(ReadOnlyModelViewSet):
    renderer_classes = [JSONRenderer]

    @method_decorator(cache_page(settings.CACHE_SECONDS))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(settings.CACHE_SECONDS))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

class ResourceViewSet(CachedReadOnlyModelViewSet):
    queryset = Resource.objects.order_by('name').all()
    serializer_class = ResourceSerializer

class PersonViewSet(CachedReadOnlyModelViewSet):
    queryset = Person.objects.order_by('fullname').all()
    serializer_class = PersonSerializer

class OrganizationViewSet(CachedReadOnlyModelViewSet):
    queryset = Organization.objects.order_by('name').all()
    serializer_class = OrganizationSerializer

router = DefaultRouter(use_regex_path=False, trailing_slash=False)
router.register('resources', ResourceViewSet)
router.register('people', PersonViewSet)
router.register('organizations', OrganizationViewSet)