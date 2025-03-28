# Generated by Django 5.1.4 on 2025-03-21 02:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('exams', '0001_initial'),
        ('questions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField()),
                ('total_questions', models.IntegerField()),
                ('correct_answers', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.exam')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selected_option', models.CharField(max_length=1)),
                ('is_correct', models.BooleanField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.question')),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='results.result')),
            ],
        ),
    ]
