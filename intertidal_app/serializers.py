from rest_framework import serializers


from .models import Resource, Person, Organization

class OrganizationSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    class Meta:
        model = Organization
        fields = ['id', 'label', 'alternative_names', 'address', 'links']
    def get_label(self, obj):
        return obj.name

class PersonSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    thumbnail = serializers.ImageField(read_only=True)
    class Meta:
        model = Person
        fields = ['id', 'label', 'citation_key', 'alternative_names', 'links', 'bio', 'image', 'thumbnail']
    def get_label(self, obj):
        return obj.fullname

class ResourceSerializer(serializers.ModelSerializer):
    person_ids = serializers.SerializerMethodField()
    organization_ids = serializers.SerializerMethodField()
    thumbnail = serializers.SerializerMethodField()

    class Meta:
        model = Resource
        fields = [
            'id', 'name', # 'alternative_names', 'description', 'links',
            'locale', 'categories', # 'forms', 'keywords', 'language',
            # 'date', 'date_end', 'date_current',
            'person_ids', 'organization_ids', 'thumbnail',
        ]

    def get_person_ids(self, obj):
        person_ids = [person_responsibility_statement.person_id for person_responsibility_statement in obj.person_responsibility_statements.all()]
        for edition in obj.editions.all():
            person_ids += [person_responsibility_statement.person_id for person_responsibility_statement in edition.person_responsibility_statements.all()]
        for occurrence in obj.occurrences.all():
            person_ids += [person_responsibility_statement.person_id for person_responsibility_statement in occurrence.person_responsibility_statements.all()]
        return list(set(person_ids))

    def get_organization_ids(self, obj):
        organization_ids = [organization_responsibility_statement.organization_id for organization_responsibility_statement in obj.organization_responsibility_statements.all()]
        for edition in obj.editions.all():
            organization_ids += [organization_responsibility_statement.organization_id for organization_responsibility_statement in edition.organization_responsibility_statements.all()]
        for occurrence in obj.occurrences.all():
            organization_ids += [organization_responsibility_statement.organization_id for organization_responsibility_statement in occurrence.organization_responsibility_statements.all()]
        return list(set(organization_ids))

    def get_thumbnail(self, obj):
        image = obj.images.first()
        return image.thumbnail.url if image and image.image else None