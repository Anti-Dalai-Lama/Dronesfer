from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class Drone(models.Model):
    model = models.CharField(max_length=200)
    weight = models.FloatField(validators = [MinValueValidator(0.0)])
    add_weight = models.FloatField(validators = [MinValueValidator(0.0)])
    speed = models.FloatField(validators = [MinValueValidator(0.0)])

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
    load_weight = models.FloatField(validators = [MinValueValidator(0.0)])
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField()
    distance = models.FloatField(validators = [MinValueValidator(0.0)])
    start_point = models.OneToOneField(Location, related_name="start_point")
    end_point = models.OneToOneField(Location, related_name="end_point")

    def __str__(self):
        return self.load_title
