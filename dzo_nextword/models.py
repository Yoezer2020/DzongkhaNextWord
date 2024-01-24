# models.py

from django.db import models

class UserInput(models.Model):
    seed_text = models.CharField(max_length=255)
    top_n = models.IntegerField(default=1)
    prediction = models.TextField(blank=True)
