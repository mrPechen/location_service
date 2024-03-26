from geopy.distance import geodesic

from api.models import Car


class CarServices:

    @classmethod
    def get_nearby_cars(cls, obj, filter_radius: int | None):
        cargo_pickup_location = (obj.pick_up_location.latitude, obj.pick_up_location.longitude)


        radius = 450
        if filter_radius is not None:
            radius = filter_radius

        # Вычисляем координаты точек на краях квадрата
        lat_deg = geodesic(miles=radius).destination(cargo_pickup_location, 0).latitude
        lon_deg = geodesic(miles=radius).destination(cargo_pickup_location, 90).longitude
        min_lat = cargo_pickup_location[0] - (lat_deg - cargo_pickup_location[0])
        max_lat = cargo_pickup_location[0] + (lat_deg - cargo_pickup_location[0])
        min_lon = cargo_pickup_location[1] - (lon_deg - cargo_pickup_location[1])
        max_lon = cargo_pickup_location[1] + (lon_deg - cargo_pickup_location[1])

        # Фильтруем машины в указанном прямоугольнике
        result = Car.objects.filter(
            location__latitude__range=(min_lat, max_lat),
            location__longitude__range=(min_lon, max_lon)
        )
        return result
