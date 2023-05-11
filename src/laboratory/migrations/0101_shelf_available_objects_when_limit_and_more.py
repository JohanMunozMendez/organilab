# Generated by Django 4.1.9 on 2023-05-10 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laboratory', '0100_furniture_creator_laboratory_creator_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shelf',
            name='available_objects_when_limit',
            field=models.ManyToManyField(related_name='limit_objects', to='laboratory.shelfobject', verbose_name='Only objects allowed in this shelf'),
        ),
        migrations.AddField(
            model_name='shelf',
            name='limit_only_objects',
            field=models.BooleanField(default=False, verbose_name='Limit objects to be added'),
        ),
    ]
