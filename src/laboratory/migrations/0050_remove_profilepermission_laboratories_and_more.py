# Generated by Django 4.0.8 on 2022-10-19 06:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth_and_perms', '0003_update_sequences'),
        ('laboratory', '0049_alter_organizationstructure_managers_and_more'),
    ]

    operations = [
        migrations.RunSQL(
            "DROP TABLE IF EXISTS laboratory_profile;",
            state_operations=[  migrations.DeleteModel(
                                    name='Profile',
                                )
            ],
        ),

        migrations.RunSQL(
            "DROP TABLE IF EXISTS laboratory_rol;",
            state_operations=[migrations.DeleteModel(
                name='Rol',
            )
            ],
        ),

        migrations.DeleteModel(
            name='ProfilePermission',
        ),

    ]
