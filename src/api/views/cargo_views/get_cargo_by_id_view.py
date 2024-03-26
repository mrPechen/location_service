from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from geopy.distance import distance
from rest_framework.fields import SerializerMethodField
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView

from api.models import Car, Cargo, Location
from api.services.car_services import CarServices


class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = ['city', 'state_name', 'zip', 'latitude', 'longitude']


class GetCargoView(APIView):
    class OutputSerializer(ModelSerializer):
        class CarSerializer(ModelSerializer):
            distance_in_miles = SerializerMethodField()
            location = LocationSerializer(read_only=True)

            class Meta:
                model = Car
                fields = '__all__'
                ref_name = "CarSerializer for cargo"

            def get_distance_in_miles(self, obj):
                cargo_location = self.context['cargo_location']
                car_location = (obj.location.latitude, obj.location.longitude)
                result = distance(car_location, cargo_location).miles
                return result

        cars = SerializerMethodField()
        pick_up_location = LocationSerializer(read_only=True)
        delivery_location = LocationSerializer(read_only=True)

        class Meta:
            model = Cargo
            fields = ['pick_up_location', 'delivery_location',
                      'weight', 'description', 'cars']
            ref_name = "OutputSerializer for cargo"

        def get_cars(self, obj):
            cargo_pickup_location = (obj.pick_up_location.latitude, obj.pick_up_location.longitude)
            data = CarServices.get_nearby_cars(obj, filter_radius=None)
            serializer = self.CarSerializer(data, many=True, context={
                'cargo_location': cargo_pickup_location})
            return serializer.data

    @swagger_auto_schema(responses={
        200: OutputSerializer,
        404: "Not found",
    }, tags=["cargo"],
    )
    def get(self, request, cargo_id: int):
        data = get_object_or_404(Cargo, id=cargo_id)
        serializer = self.OutputSerializer(data)
        return Response(serializer.data)