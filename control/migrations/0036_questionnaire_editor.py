# Generated by Django 2.2.5 on 2019-11-04 15:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('control', '0035_change_some_labels'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionnaire',
            name='editor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='questionnaires', to=settings.AUTH_USER_MODEL),
        ),
    ]
