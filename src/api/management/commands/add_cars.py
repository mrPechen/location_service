import random

from django.core.management.base import BaseCommand

from api.models import Car, Location


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        locations = Location.objects.all()

        for _ in range(20):
            random_location = random.choice(locations)
            random_capacity = random.randint(1, 1000)
            Car.objects.create(location=random_location, capacity=random_capacity)

