import json

from django.views.generic import TemplateView, DetailView, ListView
from django.templatetags.static import static
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Count

from .marc_relators import MarcRelator
from .models import Resource, Person, Organization, ResourceAudio
from .schema import ResourceSchema, PersonStubSchema, OrganizationStubSchema

def home(request):
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


    ambient_soundscape = {
        'url': static('audio/intertidal_draft_ambient_soundscape.ogg'),
        'title': 'Ambient Soundscape',
    }
    roundtable_interview_resources = Resource.objects \
        .prefetch_related('audios') \
        .annotate(total_audios=Count('audios')) \
        .filter(total_audios__gte=1) \
        .filter(categories__contains=[Resource.CategoryTypes.ROUNDTABLE_INTERVIEW]) \
        .order_by('name') \
        .all()

    playlist = [ambient_soundscape] + [{
        'url': resource.audios.first().audio.url,
        'title': resource.name,
        'resource_url': reverse('resource-details', kwargs={'pk': resource.pk}),
    } for resource in roundtable_interview_resources]

    return render(request, f'index.html', {
        'playlist_json': json.dumps(playlist),
        'resources_json': json.dumps([ResourceSchema.from_orm(resource).dict() for resource in resources]),
        'people_json': json.dumps([PersonStubSchema.from_orm(person).dict() for person in people]),
        'organizations_json': json.dumps([OrganizationStubSchema.from_orm(organization).dict() for organization in organizations]),
        'marc_relators_json': json.dumps(MarcRelator.choices),
    })

class ResourceDetailsView(DetailView):
    model = Resource
    template_name = 'resourceDetails.html'

    def get_template_names(self):
        if Resource.CategoryTypes.ROUNDTABLE_INTERVIEW in self.object.categories:
            return ['resourceRoundtableInterviewDetails.html']
        return super().get_template_names()

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