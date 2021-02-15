# Generated by Django 2.2.4 on 2019-08-05 19:41

from django.conf import settings
from django.db import migrations
import django.db.models.deletion
import isc_common.fields.related


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0026_auto_20190805_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages_theme_access',
            name='theme',
            field=isc_common.fields.related.ForeignKeyCascade(on_delete=django.db.models.deletion.CASCADE, to='tracker.Messages_theme'),
        ),
        migrations.AlterField(
            model_name='messages_theme_access',
            name='user',
            field=isc_common.fields.related.ForeignKeyCascade(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
