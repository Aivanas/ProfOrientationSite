# Generated by Django 4.2 on 2024-10-01 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StudyPlatform', '0004_choice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
