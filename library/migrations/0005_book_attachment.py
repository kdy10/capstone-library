# Generated by Django 5.1.4 on 2024-12-17 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_alter_book_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to='attachments/'),
        ),
    ]