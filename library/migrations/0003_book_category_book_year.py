# Generated by Django 5.1.4 on 2024-12-17 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_book_is_archived'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.CharField(default='General', max_length=100),
        ),
        migrations.AddField(
            model_name='book',
            name='year',
            field=models.IntegerField(default=2024),
        ),
    ]