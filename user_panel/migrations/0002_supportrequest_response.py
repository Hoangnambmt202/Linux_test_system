# Generated by Django 5.1.4 on 2025-03-25 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_panel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='supportrequest',
            name='response',
            field=models.TextField(blank=True, null=True),
        ),
    ]
