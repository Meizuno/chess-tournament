# Generated by Django 4.2 on 2023-05-15 06:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_remove_tournament_organizer_tournament_organizers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='country',
            field=models.CharField(max_length=3, verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='player',
            name='username',
            field=models.CharField(default='', max_length=30, unique=True, verbose_name='Username'),
        ),
        migrations.AlterField(
            model_name='tournament',
            name='organizers',
            field=models.ManyToManyField(related_name='organized_tournaments', to=settings.AUTH_USER_MODEL),
        ),
    ]