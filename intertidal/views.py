import json

from django.views.generic import TemplateView, DetailView, ListView
from django.templatetags.static import static
from django.shortcuts import render
from .models import Resource, Person, Organization
from .schema import ResourceStubSchema, PersonStubSchema, OrganizationStubSchema


def home(request):
    return render(request, 'index.html')

def mockup(request, version):
    chapters = [
        {'title': 'Waves (Segment 1)', 'startTime': 0, 'endTime': 44 },
        {'title': 'Metal Hinge (Segment 2)', 'startTime': 44, 'endTime': 92 },
        {'title': 'Etc (Segment 3)', 'startTime': 92, 'endTime': 267 },
    ]
    audio = [
        { 'name': 'Test Audio 1', 'url': static('audio/intertidal_draft_ambient_soundscape.ogg') },
        { 'name': 'Test Audio 2', 'url': static('audio/intertidal_draft_ambient_soundscape.ogg') },
        { 'name': 'Test Audio 3', 'url': static('audio/intertidal_draft_ambient_soundscape.ogg') },
        { 'name': 'Test Audio 4', 'url': static('audio/intertidal_draft_ambient_soundscape.ogg') },
        { 'name': 'Test Audio 5', 'url': static('audio/intertidal_draft_ambient_soundscape.ogg') },
        { 'name': 'Test Audio 6', 'url': static('audio/intertidal_draft_ambient_soundscape.ogg') },
        { 'name': 'Test Audio 7', 'url': static('audio/intertidal_draft_ambient_soundscape.ogg') },
        { 'name': 'Test Audio 8', 'url': static('audio/intertidal_draft_ambient_soundscape.ogg') },
        { 'name': 'Test Audio 9', 'url': static('audio/intertidal_draft_ambient_soundscape.ogg') },
        { 'name': 'Test Audio 10', 'url': static('audio/intertidal_draft_ambient_soundscape.ogg') },
    ]
    resources = Resource.objects.prefetch_related(
        'person_responsibility_statements', 'organization_responsibility_statements',

        'editions',
        'editions__person_responsibility_statements', 'editions__organization_responsibility_statements',

        'occurrences',
        'occurrences__person_responsibility_statements', 'occurrences__organization_responsibility_statements',

        'audios',
        'images',
    ).order_by('name').all()
    people = Person.objects.order_by('fullname').all()
    organizations = Organization.objects.order_by('name').all()

    return render(request, f'mockup/{version}.html', {
        'chapters_json': json.dumps(chapters),
        'audio_json': json.dumps(audio),
        'resources': resources,
        'resources_json': json.dumps([ResourceStubSchema.from_orm(resource).dict() for resource in  resources]),
        'people_json': json.dumps([PersonStubSchema.from_orm(person).dict() for person in people]),
        'organizations_json': json.dumps([OrganizationStubSchema.from_orm(organization).dict() for organization in organizations]),
    })

class ResourceDetailsView(DetailView):
    model = Resource
    template_name = 'resourceDetails.html'

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).prefetch_related(
            'person_responsibility_statements', 'organization_responsibility_statements',

            'editions',
            'editions__person_responsibility_statements', 'editions__organization_responsibility_statements',

            'occurrences',
            'occurrences__person_responsibility_statements', 'occurrences__organization_responsibility_statements',

            'audios',
            'images',
        )