# Generated by Django 4.2 on 2023-05-18 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_remove_player_lang_remove_player_theme_player_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='images/foto/'),
        ),
    ]