# Generated by Django 2.0.3 on 2018-06-09 10:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mla',
            old_name='password',
            new_name='hashed_password',
        ),
    ]
