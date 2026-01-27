from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.forms import SimpleArrayField, SplitArrayField
from partial_date import PartialDateField
from django.conf.global_settings import LANGUAGES
from intertidal.marc_relators import MarcRelator
from intertidal.cls_types import ClsTypes
from django.utils.safestring import mark_safe
from django_advance_thumbnail import AdvanceThumbnailField

class SimpleArrayFieldSelect2Fix(SimpleArrayField):
    def prepare_value(self, value):
        if isinstance(value, list):
            return self.delimiter.join(
                str(f'"{self.base_field.prepare_value(v)}"') for v in value
            )
        return value

class AlternativeNamesArrayField(ArrayField):
    def formfield(self, **kwargs):
        defaults = {
            'form_class': SimpleArrayFieldSelect2Fix,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)


class Person(models.Model):
    # fields
    fullname = models.CharField(db_index=True)
    citation_key = models.CharField(db_index=True, blank=True)
    alternative_names = AlternativeNamesArrayField(models.CharField(), default=list, blank=True)
    links = ArrayField(models.CharField(), default=list, blank=True)
    bio = models.TextField(blank=True)

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
        name = self.citation_key if self.citation_key else self.fullname
        return f"{name}  ({self.get_alternative_names_short()})" if self.get_alternative_names_short() else name

class Organization(models.Model):
    # fields
    name = models.CharField(db_index=True)
    alternative_names = AlternativeNamesArrayField(models.CharField(), default=list, blank=True)
    address = models.CharField(blank=True)
    links = ArrayField(models.CharField(), default=list, blank=True)

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

    def __str__(self):
        return f'{self.person if self.person else 'N/A'} ({', '.join([MarcRelator(marc_relator).label for marc_relator in self.marc_relators])})'

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

    def __str__(self):
        return f'{self.organization if self.organization else 'N/A'} ({', '.join([MarcRelator(marc_relator).label for marc_relator in self.marc_relators])})'

class Resource(models.Model):
    class LocaleTypes(models.TextChoices):
        VANCOUVER = "VANCOUVER", "Vancouver"
        SINGAPORE = "SINGAPORE", "Singapore"
        HONG_KONG = "HONG_KONG", "Hong Kong"

    class CategoryTypes(models.TextChoices):
        LITERARY_WORK = "LITERARY_WORK", "Literary Work"
        ART_PERFORMANCE = "ART_PERFORMANCE", "Art/Performance"
        STATE_ARCHITECTURE_MISC = "STATE_ARCHITECTURE_MISC", "State/Architecture/Misc."
        NEWS_DOCUMENTARY = "NEWS_DOCUMENTARY", "News/Documentary"
        ACADEMIC_RESEARCH = "ACADEMIC_RESEARCH", "Academic Research"
        SOCIAL_MEDIA = "SOCIAL_MEDIA", "Social Media"
        ROUNDTABLE_INTERVIEW = "ROUNDTABLE_INTERVIEW", "Roundtable/Interview"
        FIELD_RECORDING = "FIELD_RECORDING", "Field Recording"

    # fields
    locale = models.CharField(
        choices=LocaleTypes.choices,
        default=LocaleTypes.VANCOUVER,
        db_index=True,
    )
    categories = ArrayField(
        models.CharField(choices=CategoryTypes.choices),
        default=list,
        db_index=True,
    )
    name = models.CharField(db_index=True, verbose_name='Name/Title')
    alternative_names = AlternativeNamesArrayField(models.CharField(), default=list, blank=True, verbose_name='Alternative Names/Titles')
    language = models.CharField(
        choices=LANGUAGES,
        default='en',
        blank=True,
    )
    forms = ArrayField(
        models.CharField(choices=ClsTypes.choices), default=list, blank=True, verbose_name='Physical/Digital Forms',
        help_text=mark_safe('See the list of <u><a href="https://docs.citationstyles.org/en/stable/specification.html#appendix-iii-types" target="_blank">Citation Style Language Types</a></u> for descriptions of each form')
    )
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

    def save(self, *args, **kwargs):
        # change keywords to lowercase
        if self.keywords and len(self.keywords) > 0:
            self.keywords = [k.lower() for k in self.keywords]

        # save
        super().save(*args, **kwargs)

    def get_locale_choice(self):
        return self.LocaleTypes(self.locale) if self.locale else None

    def get_category_choices(self):
        return [self.CategoryTypes(category) for category in self.categories]

    def get_form_choices(self):
        return [ClsTypes(form) for form in self.forms]

    def get_contributors(self):
        results = []

        for person_responsibility_statement in self.person_responsibility_statements.all():
            results.append({
                'statement_type': 'person',
                'id': person_responsibility_statement.person.id,
                'label': person_responsibility_statement.person.fullname,
                'marc_relator_choices': [MarcRelator(marc_relator) for marc_relator in person_responsibility_statement.marc_relators],
            })

        for organization_responsibility_statement in self.organization_responsibility_statements.all():
            results.append({
                'statement_type': 'organization',
                'id': organization_responsibility_statement.organization.id,
                'label': organization_responsibility_statement.organization.name,
                'marc_relator_choices': [MarcRelator(marc_relator) for marc_relator in organization_responsibility_statement.marc_relators],
            })

        return sorted(results, key=lambda item: item['label'])

class Edition(models.Model):
    # fields
    name = models.CharField(verbose_name='Name/Title', blank=True)
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

    def get_contributors(self):
        results = []

        for person_responsibility_statement in self.person_responsibility_statements.all():
            results.append({
                'statement_type': 'person',
                'id': person_responsibility_statement.person.id,
                'label': person_responsibility_statement.person.fullname,
                'marc_relator_choices': [MarcRelator(marc_relator) for marc_relator in person_responsibility_statement.marc_relators],
            })

        for organization_responsibility_statement in self.organization_responsibility_statements.all():
            results.append({
                'statement_type': 'organization',
                'id': organization_responsibility_statement.organization.id,
                'label': organization_responsibility_statement.organization.name,
                'marc_relator_choices': [MarcRelator(marc_relator) for marc_relator in organization_responsibility_statement.marc_relators],
            })

        return sorted(results, key=lambda item: item['label'])

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
        on_delete=models.CASCADE,
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

    class Meta:
        verbose_name = "Special Occurrence"

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

    def get_contributors(self):
        results = []

        for person_responsibility_statement in self.person_responsibility_statements.all():
            results.append({
                'statement_type': 'person',
                'id': person_responsibility_statement.person.id,
                'label': person_responsibility_statement.person.fullname,
                'marc_relator_choices': [MarcRelator(marc_relator) for marc_relator in person_responsibility_statement.marc_relators],
            })

        for organization_responsibility_statement in self.organization_responsibility_statements.all():
            results.append({
                'statement_type': 'organization',
                'id': organization_responsibility_statement.organization.id,
                'label': organization_responsibility_statement.organization.name,
                'marc_relator_choices': [MarcRelator(marc_relator) for marc_relator in organization_responsibility_statement.marc_relators],
            })

        return sorted(results, key=lambda item: item['label'])

class ResourceAudio(models.Model):
    name = models.CharField(verbose_name='File Name', blank=True)
    audio = models.FileField(
        upload_to='audio/',
        null=True,
        blank=True,
        help_text=mark_safe('Please use <u><a href="https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Containers" target="_blank">standard web audio types</a></u>. MP3 (.mp3), WAV (.wav), or Ogg (.ogg) are recommended.'),
    )
    transcript = models.TextField(blank=True, verbose_name='Transcript')

    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    # relationships
    resource = models.ForeignKey(
        Resource,
        related_name='audios',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

class ResourceImage(models.Model):
    name = models.CharField(verbose_name='File Name', blank=True)
    image = models.ImageField(
        upload_to='images/',
        width_field='image_width',
        height_field='image_height',
        help_text=mark_safe('Please use <u><a href="https://developer.mozilla.org/en-US/docs/Web/Media/Formats/Image_types" target="_blank">standard web image types</a></u>. PNG, JPEG, and WebP are recommended.'),
    )
    image_width = models.IntegerField(
        null=True,
        blank=True,
    )
    image_height = models.IntegerField(
        null=True,
        blank=True,
    )
    thumbnail = AdvanceThumbnailField(
        source_field='image',
        upload_to='thumbnails/',
        null=True,
        blank=True,
        size=(520, 520),
    )

    # write tracking fields
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    # relationships
    resource = models.ForeignKey(
        Resource,
        related_name='images',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name