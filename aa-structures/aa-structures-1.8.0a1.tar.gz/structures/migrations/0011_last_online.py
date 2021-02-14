# Generated by Django 2.2.12 on 2020-05-26 14:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("structures", "0010_sovereignty_map"),
    ]

    operations = [
        migrations.RenameField(
            model_name="structure",
            old_name="fuel_expires",
            new_name="fuel_expires_at",
        ),
        migrations.RenameField(
            model_name="structure",
            old_name="last_updated",
            new_name="last_updated_at",
        ),
        migrations.AddField(
            model_name="structure",
            name="created_at",
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                help_text="date this structure was received from ESI for the first time",
            ),
        ),
        migrations.AddField(
            model_name="structure",
            name="last_online_at",
            field=models.DateTimeField(
                blank=True,
                default=None,
                help_text="date this structure had any of it's services online",
                null=True,
            ),
        ),
    ]
