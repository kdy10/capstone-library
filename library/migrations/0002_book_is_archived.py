# Generated by Django 5.1.4 on 2024-12-12 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='is_archived',
            field=models.BooleanField(default=False),
        ),
    ]