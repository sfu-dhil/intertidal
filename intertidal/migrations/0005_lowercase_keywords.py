# Generated by Django 5.1.7 on 2025-04-15 19:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('intertidal', '0004_remove_organization_emails_remove_person_emails_and_more'),
    ]

    operations = [
        migrations.RunSQL(sql='''
            UPDATE intertidal_resource
            SET keywords = LOWER(keywords::TEXT)::TEXT[]
            WHERE keywords IS NOT NULL
        ''')
    ]
