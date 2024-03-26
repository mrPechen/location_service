from django.contrib import admin

from api.models import Location, Car, Cargo


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    show_on_dispaly = '__all__'


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    show_on_dispaly = '__all__'


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    show_on_dispaly = '__all__'
