# Generated by Django 4.0.5 on 2022-06-25 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('semesters', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='semesters',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
