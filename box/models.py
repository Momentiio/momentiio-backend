from django.db import models
from fly.models import Fly


class Box(models.Model):
    title = models.CharField(max_length=150)
    fly = models.ManyToMany(Fly, on_delete=models.CASCADE)
