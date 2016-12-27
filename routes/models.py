from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
from django.utils import timezone

# Create your models here.

class Drone(models.Model):
    model = models.CharField(max_length=200)
    weight = models.DecimalField(validators = [MinValueValidator(0.0)], decimal_places=3, max_digits=6)
    add_weight = models.DecimalField(validators = [MinValueValidator(0.0)], decimal_places=3, max_digits=6)
    speed = models.DecimalField(validators = [MinValueValidator(0.0)], decimal_places=2, max_digits=5)

    def __str__(self):
        return self.model


class Location(models.Model):
    title = models.CharField(max_length=500)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.title


class Route(models.Model):
    load_title = models.CharField(max_length=200)
    load_weight = models.DecimalField(validators = [MinValueValidator(0.0)], decimal_places=3, max_digits=6)
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField()
    end_time = models.DateTimeField(default=timezone.now)
    distance = models.IntegerField(validators = [MinValueValidator(0.0)])
    start_point = models.OneToOneField(Location, related_name="start_point")
    end_point = models.OneToOneField(Location, related_name="end_point")
    price = models.DecimalField(validators = [MinValueValidator(0.0)], default=0, decimal_places=2, max_digits=6)

    def __str__(self):
        return self.load_title
