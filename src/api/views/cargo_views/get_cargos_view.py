from drf_yasg.utils import swagger_auto_schema
from geopy.distance import distance
from rest_framework.fields import SerializerMethodField
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, Serializer, IntegerField, FloatField
from rest_framework.views import APIView

from api.models import Car, Cargo, Location
from api.services.car_services import CarServices


class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = ['city', 'state_name', 'zip', 'latitude', 'longitude']
        ref_name = "LocationSerializer for cargos"


class GetCargosView(APIView):
    class QueryParamsSerializer(Serializer):
        weight = IntegerField(required=False)
        radius = IntegerField(required=False)

        class Meta:
            ref_name = "QueryParamsSerializer for cargos"

    class OutputSerializer(ModelSerializer):
        class CarSerializer(ModelSerializer):
            distance_in_miles = SerializerMethodField()
            location = LocationSerializer(read_only=True)

            class Meta:
                model = Car
                fields = '__all__'
                ref_name = "CarSerializer for cargos"

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
            fields = ['id', 'pick_up_location', 'delivery_location',
                      'weight', 'description', 'cars']
            ref_name = "OutputSerializer for cargos"

        def get_cars(self, obj):
            cargo_pickup_location = (obj.pick_up_location.latitude, obj.pick_up_location.longitude)
            data = CarServices.get_nearby_cars(obj, self.context['radius_filter'])
            serializer = self.CarSerializer(data, many=True, context={
                'cargo_location': cargo_pickup_location})
            return serializer.data

    @swagger_auto_schema(responses={
        200: OutputSerializer,
    }, tags=["cargo"], query_serializer=QueryParamsSerializer()
    )
    def get(self, request):
        params = self.QueryParamsSerializer(data=request.GET)
        params.is_valid(raise_exception=True)
        data = Cargo.objects.all()
        cargo_weight = params.data.get('weight')
        if cargo_weight is not None:
            data = Cargo.objects.filter(weight__lte=cargo_weight)
        serializer = self.OutputSerializer(data, many=True, context={"radius_filter": params.data.get('radius')})
        return Response(serializer.data)
