# Generated by Django 4.0.8 on 2023-07-06 04:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sga', '0062_remove_displaylabel_user_remove_substance_creator_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            "ALTER TABLE sga_builderinformation ADD IF NOT EXISTS user_id INTEGER;",
            state_operations=[
                migrations.AddField(
                    "builderinformation",
                    "user",
                    models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_bi', to=settings.AUTH_USER_MODEL, verbose_name='User'),
                ),
            ],
        ),
        migrations.AlterField(
            model_name='builderinformation',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='displaylabel',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='substance',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='templatesga',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
