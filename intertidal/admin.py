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
from intertidal.widgets import PartialDateWidget, Select2ChoiceArrayWidget, Select2TagArrayWidget, Select2TagWithCommaArrayWidget
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
        'bio',
    ]
    list_display = ('fullname', 'citation_key', 'alternative_names')
    list_display_links = ('fullname', 'citation_key', 'alternative_names')
    ordering = ['fullname', 'citation_key']
    search_fields = ['fullname', 'citation_key', 'alternative_names']
    formfield_overrides = {
        TextField: {'widget': TinyMCE},
    }

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'alternative_names':
            kwargs['widget'] = Select2TagWithCommaArrayWidget(attrs={
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
    ]
    list_display = ('name', 'alternative_names')
    list_display_links = ('name', 'alternative_names')
    ordering = ['name']
    search_fields = ['name', 'alternative_names']

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'alternative_names':
            kwargs['widget'] = Select2TagWithCommaArrayWidget(attrs={
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

class CategoriesListFilter(admin.SimpleListFilter):
    title = "categories"
    parameter_name = "categories"

    def lookups(self, request, model_admin):
        return Resource.CategoryTypes.choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(categories__contains=[self.value()])

class FormsListFilter(admin.SimpleListFilter):
    title = "Forms"
    parameter_name = "forms"

    def lookups(self, request, model_admin):
        return ClsTypes.choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(forms__contains=[self.value()])

class KeywordsListFilter(admin.SimpleListFilter):
    title = "keywords"
    parameter_name = "keywords"

    def lookups(self, request, model_admin):
        keywords = [
            kw
            for subgroup in Resource.objects.values_list('keywords', flat=True)
            for kw in subgroup
        ]
        return [(kw, kw) for kw in set(keywords)]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(keywords__contains=[self.value()])

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
                'keywords',
                'links',
            )
        }),
        ('Description/Notes', {
            'classes': ['collapse'],
            'fields': ('description', 'notes'),
        }),
    )
    list_filter = ['locale', 'language', CategoriesListFilter, FormsListFilter, KeywordsListFilter]
    list_display = ('name', 'alternative_names', 'date')
    list_display_links = ('name', 'alternative_names', 'date')
    ordering = ['locale', 'name']
    search_fields = ['name', 'alternative_names', 'description', 'notes']
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
            kwargs['widget'] = Select2TagWithCommaArrayWidget(attrs={
                'data-placeholder': 'Click to add one or more alternative names',
            })
        elif db_field.name == 'forms':
            kwargs['widget'] = Select2ChoiceArrayWidget(
                attrs={
                    'data-placeholder': 'Click to select one or more forms',
                },
                choices=ClsTypes.choices,
            )
        elif db_field.name == 'keywords':
            kwargs['widget'] = Select2TagArrayWidget(attrs={
                'data-placeholder': 'Click to add one or more keywords',
            })
        elif db_field.name == 'links':
            kwargs['widget'] = Select2TagArrayWidget(attrs={
                'data-placeholder': 'Click to add one or more links',
            })
        return super().formfield_for_dbfield(db_field, **kwargs)
