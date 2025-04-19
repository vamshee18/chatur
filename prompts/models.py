from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Prompt(models.Model):
    CATEGORY_CHOICES = [
        ('career', 'Career'),
        ('study', 'Study'),
        ('social', 'Social Media'),
        ('coding', 'Coding'),
        ('other', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    prompt_text = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    tags = models.CharField(max_length=200, blank=True, help_text="Comma-separated tags like ai, productivity, writing")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
