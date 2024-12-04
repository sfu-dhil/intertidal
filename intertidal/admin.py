from django.contrib import admin
from partial_date import PartialDateField
from django.db.models import TextField
from django.contrib.postgres.fields import ArrayField
from nested_admin.nested import NestedModelAdmin, NestedTabularInline, NestedGenericTabularInline
from datetime import datetime
from django.utils.safestring import mark_safe
from tinymce.widgets import TinyMCE

from intertidal.models import Resource, Edition, Occurrence, \
    PersonResponsibilityStatement, Person, \
    OrganizationResponsibilityStatement, Organization, \
    ResourceImage, ResourceAudio
from intertidal.widgets import PartialDateWidget, Select2ChoiceArrayWidget, Select2TagArrayWidget
from intertidal.marc_relators import MarcRelator
from intertidal.cls_types import ClsTypes

PARTIAL_DATE_WIDGET_YEARS = list(reversed(range(0, datetime.today().year+1)))

class PersonResponsibilityStatementInline(NestedGenericTabularInline):
    fields = ['person', 'marc_relators', 'note']
    autocomplete_fields = ['person']
    model = PersonResponsibilityStatement
    ordering = ['id']
    extra = 0
    classes = ['collapse']
    readonly_fields = ['note']
    formfield_overrides = {
        ArrayField: {
            'widget': Select2ChoiceArrayWidget(
                attrs={
                    'data-placeholder': 'Click to select one or more responsibilities',
                },
                choices=MarcRelator.choices,
            ),
        },
    }

    def note(self, obj):
        return mark_safe('See the list of <u><a href="https://www.loc.gov/marc/relators/relaterm.html" target="_blank">MARC Relators</a></u> for descriptions of each responsibility')

class OrganizationResponsibilityStatementInline(NestedGenericTabularInline):
    fields = ['organization', 'marc_relators', 'note']
    autocomplete_fields = ['organization']
    model = OrganizationResponsibilityStatement
    ordering = ['id']
    extra = 0
    classes = ['collapse']
    readonly_fields = ['note']
    formfield_overrides = {
        ArrayField: {
            'widget': Select2ChoiceArrayWidget(
                attrs={
                    'data-placeholder': 'Click to select one or more responsibilities',
                },
                choices=MarcRelator.choices,
            ),
        },
    }

    def note(self, obj):
        return mark_safe('See the list of <u><a href="https://www.loc.gov/marc/relators/relaterm.html" target="_blank">MARC Relators</a></u> for descriptions of each responsibility/role')

class EditionInlineAdmin(NestedTabularInline):
    fields = ['date', 'name']
    ordering = ['id']
    model = Edition
    extra = 0
    classes = ['collapse']
    formfield_overrides = {
        PartialDateField: {
            'widget': PartialDateWidget(years=PARTIAL_DATE_WIDGET_YEARS),
        }
    }

    inlines = [
        PersonResponsibilityStatementInline,
        OrganizationResponsibilityStatementInline,
    ]

class OccurrenceInlineAdmin(NestedTabularInline):
    fields = [
        ('date', 'date_end', 'date_current'),
        ('location', 'address')
    ]
    ordering = ['id']
    model = Occurrence
    extra = 0
    classes = ['collapse']
    formfield_overrides = {
        PartialDateField: {
            'widget': PartialDateWidget(years=PARTIAL_DATE_WIDGET_YEARS),
        }
    }

    inlines = [
        PersonResponsibilityStatementInline,
        OrganizationResponsibilityStatementInline,
    ]

class ResourceImageInlineAdmin(NestedTabularInline):
    fields = ['image']
    ordering = ['id']
    model = ResourceImage
    extra = 0
    classes = ['collapse']

class ResourceAudioInlineAdmin(NestedTabularInline):
    fields = ['audio']
    ordering = ['id']
    model = ResourceAudio
    extra = 0
    classes = ['collapse']

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    fields = [
        ('fullname', 'citation_key'),
        'alternative_names',
        'links',
        'emails',
        'bio',
    ]
    list_display = ('id', 'fullname', 'citation_key', 'alternative_names')
    list_display_links = ('id', 'fullname', 'citation_key', 'alternative_names')
    ordering = ['id', 'fullname', 'citation_key']
    search_fields = ['fullname', 'citation_key', 'alternative_names']
    formfield_overrides = {
        TextField: {'widget': TinyMCE},
    }

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'alternative_names':
            kwargs['widget'] = Select2TagArrayWidget(attrs={
                'data-placeholder': 'Click to add one or more alternative names',
            })
        elif db_field.name == 'links':
            kwargs['widget'] = Select2TagArrayWidget(attrs={
                'data-placeholder': 'Click to add one or more links',
            })
        elif db_field.name == 'emails':
            kwargs['widget'] = Select2TagArrayWidget(attrs={
                'data-placeholder': 'Click to add one or more emails',
            })
        return super().formfield_for_dbfield(db_field, **kwargs)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    fields = [
        ('name', 'alternative_names'),
        'address',
        'links',
        'emails',
    ]
    list_display = ('id', 'name', 'alternative_names')
    list_display_links = ('id', 'name', 'alternative_names')
    ordering = ['id', 'name']
    search_fields = ['name', 'alternative_names']

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'alternative_names':
            kwargs['widget'] = Select2TagArrayWidget(attrs={
                'data-placeholder': 'Click to add one or more alternative names',
            })
        elif db_field.name == 'links':
            kwargs['widget'] = Select2TagArrayWidget(attrs={
                'data-placeholder': 'Click to add one or more links',
            })
        elif db_field.name == 'emails':
            kwargs['widget'] = Select2TagArrayWidget(attrs={
                'data-placeholder': 'Click to add one or more emails',
            })
        return super().formfield_for_dbfield(db_field, **kwargs)

@admin.register(Resource)
class ResourceAdmin(NestedModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                ('locale', 'language'),
                ('name', 'alternative_names'),
                ('date', 'date_end', 'date_current'),
                'categories',
                'forms',
                'genres',
                'keywords',
                'links',
            )
        }),
        ('Description/Notes', {
            'classes': ('collapse',),
            'fields': ('description', 'notes'),
        }),
    )
    list_display = ('id', 'locale', 'language', 'name', 'alternative_names', 'date')
    list_display_links = ('id', 'locale', 'language', 'name', 'alternative_names', 'date')
    ordering = ['locale', 'name']
    search_fields = ['locale', 'language', 'name', 'alternative_names']
    formfield_overrides = {
        PartialDateField: {
            'widget': PartialDateWidget(years=PARTIAL_DATE_WIDGET_YEARS),
        },
        TextField: {
            'widget': TinyMCE
        }
    }
    inlines = [
        PersonResponsibilityStatementInline,
        OrganizationResponsibilityStatementInline,
        EditionInlineAdmin,
        OccurrenceInlineAdmin,
        ResourceImageInlineAdmin,
        ResourceAudioInlineAdmin,
    ]

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'categories':
            kwargs['widget'] = Select2ChoiceArrayWidget(
                attrs={
                    'data-placeholder': 'Click to select one or more category',
                },
                choices=Resource.CategoryTypes.choices,
            )
        elif db_field.name == 'alternative_names':
            kwargs['widget'] = Select2TagArrayWidget(attrs={
                'data-placeholder': 'Click to add one or more alternative names',
            })
        elif db_field.name == 'forms':
            kwargs['widget'] = Select2ChoiceArrayWidget(
                attrs={
                    'data-placeholder': 'Click to select one or more forms',
                },
                choices=ClsTypes.choices,
            )
        elif db_field.name == 'genres':
            kwargs['widget'] = Select2TagArrayWidget(attrs={
                'data-placeholder': 'Click to add one or more genres',
            })
        elif db_field.name == 'keywords':
            kwargs['widget'] = Select2TagArrayWidget(attrs={
                'data-placeholder': 'Click to add one or more keywords',
            })
        elif db_field.name == 'links':
            kwargs['widget'] = Select2TagArrayWidget(attrs={
                'data-placeholder': 'Click to add one or more links',
            })
        return super().formfield_for_dbfield(db_field, **kwargs)
