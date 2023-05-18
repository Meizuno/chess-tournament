# Generated by Django 4.2 on 2023-05-02 11:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_tournament_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point', models.FloatField(default=0.0, verbose_name='Points')),
                ('tie_break1', models.FloatField(default=0.0, verbose_name='Tie Break 1')),
                ('tie_break2', models.FloatField(default=0.0, verbose_name='Tie Break 1')),
                ('tie_break3', models.FloatField(default=0.0, verbose_name='Tie Break 1')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.tournament')),
            ],
        ),
    ]