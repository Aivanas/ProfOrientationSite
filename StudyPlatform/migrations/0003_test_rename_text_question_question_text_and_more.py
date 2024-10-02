# Generated by Django 4.2 on 2024-09-30 14:18

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('StudyPlatform', '0002_testmodel_question_image_alter_question_text_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('test_type', models.CharField(choices=[('psychological', 'Психологический'), ('personality', 'Личностный'), ('educational', 'Образовательный')], max_length=50)),
            ],
        ),
        migrations.RenameField(
            model_name='question',
            old_name='text',
            new_name='question_text',
        ),
        migrations.RemoveField(
            model_name='question',
            name='image',
        ),
        migrations.AddField(
            model_name='question',
            name='question_type',
            field=models.CharField(choices=[('single_choice', 'Одиночный выбор'), ('multiple_choice', 'Множественный выбор')], default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='question',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='StudyPlatform.test'),
        ),
        migrations.DeleteModel(
            name='TestModel',
        ),
    ]