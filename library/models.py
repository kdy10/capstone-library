from django.db import models

class Book(models.Model):
    CATEGORY_CHOICES = [
        ('Systems Development', 'Systems Development'),
        ('Network Administration', 'Network Administration'),
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    summary = models.TextField()
    is_archived = models.BooleanField(default=False)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='Systems Development')
    year = models.IntegerField(default=2024)
    attachment = models.FileField(upload_to='attachments/', null=True, blank=True)

    def __str__(self):
        return self.title
