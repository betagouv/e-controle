# Generated by Django 2.1.9 on 2019-07-26 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('control', '0032_reference_code_not_blank'),
    ]

    operations = [
        migrations.AddField(
            model_name='responsefile',
            name='is_deleted',
            field=models.BooleanField(default=False, help_text='Ce fichier est=il dans la corbeille?', verbose_name='Supprimé'),
        ),
    ]
