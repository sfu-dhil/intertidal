from django.db import models
from django.contrib.postgres.fields import ArrayField as DjangoArrayField
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.forms import SimpleArrayField, SplitArrayField
from partial_date import PartialDateField
from django.conf.global_settings import LANGUAGES
from intertidal.marc_relators import MarcRelator
from intertidal.cls_types import ClsTypes
from django.utils.safestring import mark_safe


class SimpleArrayFieldSelect2Fix(SimpleArrayField):
    def prepare_value(self, value):
        if isinstance(value, list):
            return '|'.join(
                str(self.base_field.prepare_value(v)) for v in value
            )
        return value


class ArrayField(DjangoArrayField):
    def formfield(self, **kwargs):
        defaults = {
            'form_class': SimpleArrayFieldSelect2Fix,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)


class Person(models.Model):
    # fields
    name = models.CharField(db_index=True)
    alternative_names = ArrayField(models.CharField(), default=list, blank=True)
    links = ArrayField(models.CharField(), default=list, blank=True)
    emails = ArrayField(models.CharField(), default=list, blank=True)

    # relationships
    # one-to-many responsibility_statements via PersonResponsibilityStatement Model

    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'people'

    def get_alternative_names_short(self):
        alternative_names = ', '.join(self.alternative_names) if len(self.alternative_names) else None
        return alternative_names[:75] + '...' if alternative_names and len(alternative_names) >= 75 else alternative_names

    def __str__(self):
        return f"{self.name} ({self.get_alternative_names_short()})" if self.get_alternative_names_short() else self.name

class Organization(models.Model):
    # fields
    name = models.CharField(db_index=True)
    alternative_names = ArrayField(models.CharField(), default=list, blank=True)
    address = models.CharField(blank=True)
    links = ArrayField(models.CharField(), default=list, blank=True)
    emails = ArrayField(models.CharField(), default=list, blank=True)

    # relationships
    # one-to-many responsibility_statements via OrganizationResponsibilityStatement Model

    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def get_alternative_names_short(self):
        alternative_names = ', '.join(self.alternative_names) if len(self.alternative_names) else None
        return alternative_names[:75] + '...' if alternative_names and len(alternative_names) >= 75 else alternative_names

    def __str__(self):
        return f"{self.name} ({self.get_alternative_names_short()})" if self.get_alternative_names_short() else self.name

class PersonResponsibilityStatement(models.Model):
    content_type = models.ForeignKey(
        ContentType,
        limit_choices_to={'model__in': ['Resource', 'Edition', 'Occurrence']},
        on_delete=models.CASCADE,
        related_name='person_responsibility_statements',
    )
    object_id = models.BigIntegerField()
    content_object = GenericForeignKey()
    person = models.ForeignKey(
        Person,
        related_name='responsibility_statements',
        on_delete=models.CASCADE
    )
    marc_relators = ArrayField(models.CharField(choices=MarcRelator.choices), default=list, verbose_name='responsibilities')

    # one-to-many resources via Resource Model
    # one-to-many editions via Edition Model
    # one-to-many occurrences via Occurrence Model

    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'intertidal_person_responsibility_statement'
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]

class OrganizationResponsibilityStatement(models.Model):
    content_type = models.ForeignKey(
        ContentType,
        limit_choices_to={'model__in': ['Resource', 'Edition', 'Occurrence']},
        on_delete=models.CASCADE,
        related_name='organization_responsibility_statements',
    )
    object_id = models.BigIntegerField()
    content_object = GenericForeignKey()
    organization = models.ForeignKey(
        Organization,
        related_name='responsibility_statements',
        on_delete=models.CASCADE
    )
    marc_relators = ArrayField(models.CharField(choices=MarcRelator.choices), default=list, verbose_name='responsibilities')

    # one-to-many resources via Resource Model
    # one-to-many editions via Edition Model
    # one-to-many occurrences via Occurrence Model

    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'intertidal_organization_responsibility_statement'
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]

class Resource(models.Model):
    class LocaleTypes(models.TextChoices):
        VANCOUVER = "VANCOUVER", "Vancouver"
        SINGAPORE = "SINGAPORE", "Singapore"
        HONG_KONG = "HONG_KONG", "Hong Kong"

    class DisplayTypes(models.TextChoices):
        LITERARY_WORK = "LITERARY_WORK", "Literary Work"
        ART_PERFORMANCE = "ART_PERFORMANCE", "Art/Performance"
        STATE_ARCHITECTURE_MISC = "STATE_ARCHITECTURE_MISC", "State/Architecture/Misc."
        NEWS_DOCUMENTARY = "NEWS_DOCUMENTARY", "News/Documentary"
        ACADEMIC_RESEARCH = "ACADEMIC_RESEARCH", "Academic Research"
        SOCIAL_MEDIA = "SOCIAL_MEDIA", "Social Media"

    # fields
    locale = models.CharField(
        choices=LocaleTypes.choices,
        default=LocaleTypes.VANCOUVER,
        db_index=True,
    )
    display_category = models.CharField(
        choices=DisplayTypes.choices,
        default=DisplayTypes.LITERARY_WORK,
        db_index=True,
    )
    name = models.CharField(db_index=True, verbose_name='Name/Title')
    alternative_names = ArrayField(models.CharField(), default=list, blank=True, verbose_name='Alternative Names/Titles')
    forms = ArrayField(
        models.CharField(choices=ClsTypes.choices), default=list, blank=True, verbose_name='Physical/Digital Forms',
        help_text=mark_safe('See the list of <a href="https://docs.citationstyles.org/en/stable/specification.html#appendix-iii-types" target="_blank">Citation Style Language Types</a> for descriptions of each form')
    )
    genres = ArrayField(models.CharField(), default=list, blank=True)
    keywords = ArrayField(models.CharField(), default=list, blank=True)
    date = PartialDateField(null=True, blank=True, db_index=True)
    date_end = PartialDateField(null=True, blank=True)
    date_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True, help_text='Notes are private (not publicly visible)')
    links = ArrayField(models.CharField(), default=list, blank=True)

    # relationships
    person_responsibility_statements = GenericRelation(
        PersonResponsibilityStatement,
        related_query_name='resource',
        related_name='resources',
    )
    organization_responsibility_statements = GenericRelation(
        OrganizationResponsibilityStatement,
        related_query_name='resource',
        related_name='resources',
    )

    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def date_str(self):
        if not self.date:
            return None
        elif self.date_current:
            return f"{self.date} - now"
        elif self.date_end:
            return f"{self.date} - {self.date_end}"
        return self.date

    def get_alternative_names_short(self):
        alternative_names = ', '.join(self.alternative_names) if len(self.alternative_names) else None
        return alternative_names[:75] + '...' if alternative_names and len(alternative_names) >= 75 else alternative_names

    def __str__(self):
        return f"{self.name} ({self.get_alternative_names_short()})" if self.get_alternative_names_short() else self.name

class Edition(models.Model):
    # fields
    name = models.CharField(verbose_name='Name/Title', blank=True)
    translation = models.BooleanField(default=False)
    translation_language = models.CharField(
        choices=LANGUAGES,
        default='en',
        blank=True,
        verbose_name='language',
    )
    date = PartialDateField(null=True, blank=True, db_index=True)

    # relationships
    resource = models.ForeignKey(
        Resource,
        related_name='editions',
        on_delete=models.CASCADE
    )
    person_responsibility_statements = GenericRelation(
        PersonResponsibilityStatement,
        related_query_name='edition',
        related_name='editions',
    )
    organization_responsibility_statements = GenericRelation(
        OrganizationResponsibilityStatement,
        related_query_name='edition',
        related_name='editions',
    )

    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.date})" if self.date else self.name

class Occurrence(models.Model):
    # fields
    location = models.CharField(blank=True, verbose_name='Location/Venue')
    address = models.CharField(blank=True)
    date = PartialDateField(null=True, blank=True, db_index=True)
    date_end = PartialDateField(null=True, blank=True)
    date_current = models.BooleanField(default=False)

    # relationships
    resource = models.ForeignKey(
        Resource,
        related_name='occurrences',
        on_delete=models.CASCADE
    )
    person_responsibility_statements = GenericRelation(
        PersonResponsibilityStatement,
        related_query_name='occurrence',
        related_name='occurrences',
    )
    organization_responsibility_statements = GenericRelation(
        OrganizationResponsibilityStatement,
        related_query_name='occurrence',
        related_name='occurrences',
    )

    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def date_str(self):
        if not self.date:
            return None
        elif self.date_current:
            return f"{self.date} - now"
        elif self.date_end:
            return f"{self.date} - {self.date_end}"
        return self.date

    def __str__(self):
        return f"{self.location} ({self.date_str()})" if self.date_str() else self.location