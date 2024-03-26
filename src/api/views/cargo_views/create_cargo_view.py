from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, IntegerField
from rest_framework.views import APIView

from api.models import Cargo, Location


class CreateCargoView(APIView):

    class InputSerializer(ModelSerializer):

        pick_up = IntegerField()
        delivery = IntegerField()

        class Meta:
            model = Cargo
            exclude = ('pick_up_location', 'delivery_location')
            ref_name = "InputSerializer for create cargo"

        def create(self, validated_data):
            pick_up_location = Location.objects.get(zip=validated_data['pick_up'])
            delivery_location = Location.objects.get(zip=validated_data['delivery'])
            cargo = Cargo(pick_up_location=pick_up_location,
                          delivery_location=delivery_location,
                          weight=validated_data['weight'],
                          description=validated_data['description'])
            cargo.save()
            print(cargo)
            return cargo

    @swagger_auto_schema(responses={
        201: InputSerializer,
        404: "Not found",
    }, tags=["cargo"],
    )
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=201)
