# Generated by Django 2.2.5 on 2019-09-09 14:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0063_auto_20190909_1357'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='messages',
            options={'ordering': ('date_create',), 'verbose_name': 'Сообщения'},
        ),
    ]
