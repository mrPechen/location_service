import pandas as pd
from django.core.management.base import BaseCommand

from api.models import Location


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        def create_locations(chunk):
            data = chunk.to_dict(orient='records')
            objects = [Location(city=row['city'], state_name=row['state_name'],
                                zip=row['zip'], latitude=row['lat'],
                                longitude=row['lng']) for row in data]
            Location.objects.bulk_create(objects)

        df = pd.read_csv('api/management/commands/uszips.csv',
                         usecols=['zip', 'lat', 'lng', 'city', 'state_name'],
                         chunksize=5000)
        for chunk in df:
            create_locations(chunk)
