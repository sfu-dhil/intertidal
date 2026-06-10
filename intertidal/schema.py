from ninja import Schema, ModelSchema, Field
from typing import List, Optional

from .models import Resource, Occurrence, Edition, \
    PersonResponsibilityStatement, OrganizationResponsibilityStatement, \
    Person, Organization, \
    ResourceImage, ResourceAudio


# stubs (for vuejs)
class PersonStubSchema(ModelSchema):
    label: str = Field(None, alias='fullname')

    class Meta:
        model = Person
        fields = [
            'id',
        ]


class OrganizationStubSchema(ModelSchema):
    label: str = Field(None, alias='name')

    class Meta:
        model = Organization
        fields = [
            'id',
        ]

class ResourceImageStubSchema(ModelSchema):
    class Meta:
        model = ResourceImage
        fields = [
            'id', 'name', 'image', 'thumbnail',
        ]

class ResourceAudioStubSchema(ModelSchema):
    class Meta:
        model = ResourceAudio
        fields = [
            'id', 'name', 'audio',
        ]

class PersonResponsibilityStatementsStubSchema(ModelSchema):
    class Meta:
        model = PersonResponsibilityStatement
        fields = [
            'person', 'marc_relators',
        ]
class OrganizationResponsibilityStatementsStubSchema(ModelSchema):
    class Meta:
        model = OrganizationResponsibilityStatement
        fields = [
            'organization', 'marc_relators',
        ]

class ResourceStubSchema(ModelSchema):
    person_ids: List[int] = []
    organization_ids: List[int] = []
    images: List[ResourceImageStubSchema] = []
    audios: List[ResourceAudioStubSchema] = []
    person_responsibility_statements: List[PersonResponsibilityStatementsStubSchema]
    organization_responsibility_statements: List[OrganizationResponsibilityStatementsStubSchema]
    date_year: Optional[int]
    date: Optional[str]
    date_end: Optional[str]

    class Meta:
        model = Resource
        fields = [
            'id', 'name',
            'locale', 'categories', 'language', 'forms', 'keywords',
            'date_current',
            # 'date_current', 'date_end', 'alternative_names', 'description', 'links',
        ]

    @staticmethod
    def resolve_date_year(obj):
        return int(obj.date.date.strftime('%Y')) if obj.date else None

    @staticmethod
    def resolve_date(obj):
        return obj.date.format('%Y', '%B %Y', '%-d %B %Y') if obj.date else None

    @staticmethod
    def resolve_date_end(obj):
        return obj.date_end.format('%Y', '%B %Y', '%-d %B %Y') if obj.date_end else None

    @staticmethod
    def resolve_person_ids(obj):
        person_ids = [person_responsibility_statement.person_id for person_responsibility_statement in obj.person_responsibility_statements.all()]
        for edition in obj.editions.all():
            person_ids += [person_responsibility_statement.person_id for person_responsibility_statement in edition.person_responsibility_statements.all()]
        for occurrence in obj.occurrences.all():
            person_ids += [person_responsibility_statement.person_id for person_responsibility_statement in occurrence.person_responsibility_statements.all()]
        return list(set(person_ids))

    @staticmethod
    def resolve_organization_ids(obj):
        organization_ids = [organization_responsibility_statement.organization_id for organization_responsibility_statement in obj.organization_responsibility_statements.all()]
        for edition in obj.editions.all():
            organization_ids += [organization_responsibility_statement.organization_id for organization_responsibility_statement in edition.organization_responsibility_statements.all()]
        for occurrence in obj.occurrences.all():
            organization_ids += [organization_responsibility_statement.organization_id for organization_responsibility_statement in occurrence.organization_responsibility_statements.all()]
        return list(set(organization_ids))
