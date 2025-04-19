from django.db import models

class Prompt(models.Model):
    title = models.CharField(max_length=100)
    prompt_text = models.TextField()

    def __str__(self):
        return self.titlse