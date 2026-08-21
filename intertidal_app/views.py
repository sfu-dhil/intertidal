import json

from django.views.generic import TemplateView, DetailView, ListView
from django.templatetags.static import static
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Count

from .models import Resource

def home(request):
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
        'url': resource.audios.first().audio_snippet.url if resource.audios.first().audio_snippet else resource.audios.first().audio.url,
        'title': resource.audios.first().name,
        'artist': resource.name,
        'resource_url': reverse('resource-details', kwargs={'pk': resource.pk}),
    } for resource in roundtable_interview_resources]

    return render(request, f'index.html', {
        'playlist_json': json.dumps(playlist),
    })

class ResourceDetailsView(DetailView):
    model = Resource
    template_name = 'resourceDetails.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['images_json'] = json.dumps([
            {
                'id': image.pk,
                'name': image.name,
                'image': image.image.url,
                'thumbnail': image.thumbnail.url,
            } for image  in self.object.images.all()
        ])
        return context

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