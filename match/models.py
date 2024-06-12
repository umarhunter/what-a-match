from django.db import models

class Integer(models.Model):
    """We need numbers"""
    number = models.IntegerField()
