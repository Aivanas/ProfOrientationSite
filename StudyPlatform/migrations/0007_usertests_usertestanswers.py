# Generated by Django 4.2 on 2024-10-02 07:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('StudyPlatform', '0006_choice_choice_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userTestTest', to='StudyPlatform.test')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userTestsUser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserTestAnswers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userAnswerChoice', to='StudyPlatform.choice')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userAnswerTest', to='StudyPlatform.test')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userAnswersUser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
