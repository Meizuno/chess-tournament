# Generated by Django 4.2 on 2023-04-26 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='date_of_birth',
            field=models.DateField(blank=True, verbose_name='Date of birth'),
        ),
    ]
