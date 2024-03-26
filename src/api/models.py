from django.core.validators import MaxValueValidator
from django.db import models


class Location(models.Model):
    class Meta:
        db_table = 'location'
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    city = models.CharField()
    state_name = models.CharField()
    zip = models.PositiveIntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"City {self.city}, id:{self.id}"


class Car(models.Model):
    class Meta:
        db_table = 'car'
        verbose_name = "Car"
        verbose_name_plural = "Cars"

    number = models.CharField(unique=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL,
                                 blank=True, null=True, related_name='car_location')
    capacity = models.PositiveIntegerField(validators=[MaxValueValidator(1000)])


class Cargo(models.Model):
    pick_up_location = models.ForeignKey(Location, on_delete=models.SET_NULL,
                                         blank=True, null=True, related_name='pick_up_location')
    delivery_location = models.ForeignKey(Location, on_delete=models.SET_NULL,
                                          blank=True, null=True, related_name='delivery_location')
    weight = models.PositiveIntegerField(validators=[MaxValueValidator(1000)])
    description = models.TextField()