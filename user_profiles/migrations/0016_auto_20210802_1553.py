# Generated by Django 2.2.13 on 2021-08-02 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profiles', '0015_auto_20210430_1509'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='useripaddress',
            options={'verbose_name': 'Adresse IP Utilisateur', 'verbose_name_plural': 'Adresses IP Utilisateurs'},
        ),
    ]
