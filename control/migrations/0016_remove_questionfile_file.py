# Generated by Django 2.1.5 on 2019-01-10 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0015_responsefile_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionfile',
            name='file',
        ),
    ]
