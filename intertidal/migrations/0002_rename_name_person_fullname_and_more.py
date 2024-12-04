# Generated by Django 5.1.3 on 2024-12-04 18:32

import django.db.models.deletion
import intertidal.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intertidal', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='name',
            new_name='fullname',
        ),
        migrations.RemoveField(
            model_name='edition',
            name='translation',
        ),
        migrations.RemoveField(
            model_name='edition',
            name='translation_language',
        ),
        migrations.RemoveField(
            model_name='resource',
            name='display_category',
        ),
        migrations.AddField(
            model_name='person',
            name='citation_key',
            field=models.CharField(blank=True, db_index=True),
        ),
        migrations.AddField(
            model_name='resource',
            name='categories',
            field=intertidal.models.ArrayField(base_field=models.CharField(choices=[('LITERARY_WORK', 'Literary Work'), ('ART_PERFORMANCE', 'Art/Performance'), ('STATE_ARCHITECTURE_MISC', 'State/Architecture/Misc.'), ('NEWS_DOCUMENTARY', 'News/Documentary'), ('ACADEMIC_RESEARCH', 'Academic Research'), ('SOCIAL_MEDIA', 'Social Media')]), db_index=True, default=list, size=None),
        ),
        migrations.AddField(
            model_name='resource',
            name='language',
            field=models.CharField(blank=True, choices=[('af', 'Afrikaans'), ('ar', 'Arabic'), ('ar-dz', 'Algerian Arabic'), ('ast', 'Asturian'), ('az', 'Azerbaijani'), ('bg', 'Bulgarian'), ('be', 'Belarusian'), ('bn', 'Bengali'), ('br', 'Breton'), ('bs', 'Bosnian'), ('ca', 'Catalan'), ('ckb', 'Central Kurdish (Sorani)'), ('cs', 'Czech'), ('cy', 'Welsh'), ('da', 'Danish'), ('de', 'German'), ('dsb', 'Lower Sorbian'), ('el', 'Greek'), ('en', 'English'), ('en-au', 'Australian English'), ('en-gb', 'British English'), ('eo', 'Esperanto'), ('es', 'Spanish'), ('es-ar', 'Argentinian Spanish'), ('es-co', 'Colombian Spanish'), ('es-mx', 'Mexican Spanish'), ('es-ni', 'Nicaraguan Spanish'), ('es-ve', 'Venezuelan Spanish'), ('et', 'Estonian'), ('eu', 'Basque'), ('fa', 'Persian'), ('fi', 'Finnish'), ('fr', 'French'), ('fy', 'Frisian'), ('ga', 'Irish'), ('gd', 'Scottish Gaelic'), ('gl', 'Galician'), ('he', 'Hebrew'), ('hi', 'Hindi'), ('hr', 'Croatian'), ('hsb', 'Upper Sorbian'), ('hu', 'Hungarian'), ('hy', 'Armenian'), ('ia', 'Interlingua'), ('id', 'Indonesian'), ('ig', 'Igbo'), ('io', 'Ido'), ('is', 'Icelandic'), ('it', 'Italian'), ('ja', 'Japanese'), ('ka', 'Georgian'), ('kab', 'Kabyle'), ('kk', 'Kazakh'), ('km', 'Khmer'), ('kn', 'Kannada'), ('ko', 'Korean'), ('ky', 'Kyrgyz'), ('lb', 'Luxembourgish'), ('lt', 'Lithuanian'), ('lv', 'Latvian'), ('mk', 'Macedonian'), ('ml', 'Malayalam'), ('mn', 'Mongolian'), ('mr', 'Marathi'), ('ms', 'Malay'), ('my', 'Burmese'), ('nb', 'Norwegian Bokmål'), ('ne', 'Nepali'), ('nl', 'Dutch'), ('nn', 'Norwegian Nynorsk'), ('os', 'Ossetic'), ('pa', 'Punjabi'), ('pl', 'Polish'), ('pt', 'Portuguese'), ('pt-br', 'Brazilian Portuguese'), ('ro', 'Romanian'), ('ru', 'Russian'), ('sk', 'Slovak'), ('sl', 'Slovenian'), ('sq', 'Albanian'), ('sr', 'Serbian'), ('sr-latn', 'Serbian Latin'), ('sv', 'Swedish'), ('sw', 'Swahili'), ('ta', 'Tamil'), ('te', 'Telugu'), ('tg', 'Tajik'), ('th', 'Thai'), ('tk', 'Turkmen'), ('tr', 'Turkish'), ('tt', 'Tatar'), ('udm', 'Udmurt'), ('ug', 'Uyghur'), ('uk', 'Ukrainian'), ('ur', 'Urdu'), ('uz', 'Uzbek'), ('vi', 'Vietnamese'), ('zh-hans', 'Simplified Chinese'), ('zh-hant', 'Traditional Chinese')], default='en'),
        ),
        migrations.AlterField(
            model_name='occurrence',
            name='resource',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='occurrences', to='intertidal.resource'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='forms',
            field=intertidal.models.ArrayField(base_field=models.CharField(choices=[('article', 'Article'), ('article_journal', 'Article Journal'), ('article_magazine', 'Article Magazine'), ('article_newspaper', 'Article Newspaper'), ('bill', 'Bill'), ('book', 'Book'), ('broadcast', 'Broadcast'), ('chapter', 'Chapter'), ('classic', 'Classic'), ('collection', 'Collection'), ('dataset', 'Dataset'), ('document', 'Document'), ('entry', 'Entry'), ('entry_dictionary', 'Entry Dictionary'), ('entry_encyclopedia', 'Entry Encyclopedia'), ('event', 'Event'), ('figure', 'Figure'), ('graphic', 'Graphic'), ('hearing', 'Hearing'), ('interview', 'Interview'), ('legal_case', 'Legal Case'), ('legislation', 'Legislation'), ('manuscript', 'Manuscript'), ('map', 'Map'), ('motion_picture', 'Motion Picture'), ('musical_score', 'Musical Score'), ('pamphlet', 'Pamphlet'), ('paper_conference', 'Paper Conference'), ('patent', 'Patent'), ('performance', 'Performance'), ('periodical', 'Periodical'), ('personal_communication', 'Personal Communication'), ('post', 'Post'), ('post_weblog', 'Post Weblog'), ('regulation', 'Regulation'), ('report', 'Report'), ('review', 'Review'), ('review_book', 'Review Book'), ('software', 'Software'), ('song', 'Song'), ('speech', 'Speech'), ('standard', 'Standard'), ('thesis', 'Thesis'), ('treaty', 'Treaty'), ('webpage', 'Webpage')]), blank=True, default=list, help_text='See the list of <u><a href="https://docs.citationstyles.org/en/stable/specification.html#appendix-iii-types" target="_blank">Citation Style Language Types</a></u> for descriptions of each form', size=None, verbose_name='Physical/Digital Forms'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='notes',
            field=models.TextField(blank=True, help_text='Notes are private (not publicly visible)'),
        ),
    ]
