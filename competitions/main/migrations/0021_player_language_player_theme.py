# Generated by Django 4.2 on 2023-05-17 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_tournament_unique_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='language',
            field=models.CharField(choices=[('en', 'English'), ('es', 'Spanish'), ('fr', 'French')], default='en', max_length=2),
        ),
        migrations.AddField(
            model_name='player',
            name='theme',
            field=models.CharField(choices=[('light', 'light'), ('dark', 'dark')], default='light', max_length=5),
        ),
    ]
