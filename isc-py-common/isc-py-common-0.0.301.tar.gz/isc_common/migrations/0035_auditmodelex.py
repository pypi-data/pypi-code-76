# Generated by Django 3.0.3 on 2020-02-08 06:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import isc_common.fields.related


class Migration(migrations.Migration):

    dependencies = [
        ('isc_common', '0034_standard_colors_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditModelEx',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='Идентификатор')),
                ('deleted_at', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Дата мягкого удаления')),
                ('editing', models.BooleanField(default=True, verbose_name='Возможность редактирования')),
                ('deliting', models.BooleanField(default=True, verbose_name='Возможность удаления')),
                ('lastmodified', models.DateTimeField(db_index=True, default=django.utils.timezone.now, editable=False, verbose_name='Последнее обновление')),
                ('creator', isc_common.fields.related.ForeignKeyProtect(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': ' Расширенная AuditModel',
            },
        ),
    ]
