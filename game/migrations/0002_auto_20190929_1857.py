# Generated by Django 2.2.1 on 2019-09-29 16:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='await',
            new_name='awaited',
        ),
    ]