import random

from root.celery import app
from api.models import Location, Car


@app.task()
def run_task():
    locations = Location.objects.all()
    cars = Car.objects.all()

    updated_cars = []
    for car in cars:
        random_location = random.choice(locations)
        car.location = random_location
        updated_cars.append(car)

    Car.objects.bulk_update(updated_cars, ['location'])