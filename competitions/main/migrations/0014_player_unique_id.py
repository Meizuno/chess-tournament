# Generated by Django 4.2 on 2023-05-16 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_alter_player_country_alter_player_username_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='unique_id',
            field=models.CharField(default=None, max_length=8, unique=True),
        ),
    ]