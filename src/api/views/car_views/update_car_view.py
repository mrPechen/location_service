from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.serializers import Serializer, IntegerField
from rest_framework.views import APIView

from api.models import Location, Car


class UpdateCarView(APIView):
    class InputSerializer(Serializer):
        zip = IntegerField()

        class Meta:
            ref_name = "InputSerializer for car update"

    @swagger_auto_schema(responses={
        200: InputSerializer,
        404: "Not found",
    }, tags=["car"],
    )
    def patch(self, request, car_id: int):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        zip = serializer.data['zip']
        car = get_object_or_404(Car, id=car_id)
        location = get_object_or_404(Location, zip=zip)
        car.location = location
        car.save()
        return Response(status=200)
