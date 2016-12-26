from django.contrib import admin
from .models import Drone, Route, Location
# Register your models here.

admin.site.register(Drone)
admin.site.register(Route)
admin.site.register(Location)