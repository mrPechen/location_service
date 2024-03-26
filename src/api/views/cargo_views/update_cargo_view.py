from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView

from api.models import Cargo


class UpdateCargoView(APIView):
    class InputSerializer(ModelSerializer):

        class Meta:
            model = Cargo
            fields = ['weight', 'description']
            ref_name = "InputSerializer for cargo update"

        def update(self, instance, validated_data):
            for name, data in validated_data.items():
                setattr(instance, name, data)
            instance.save()
            return instance

    @swagger_auto_schema(responses={
        200: InputSerializer,
        404: "Not found",
    }, tags=["cargo"],
    )
    def patch(self, request, cargo_id: int):
        cargo = get_object_or_404(Cargo, id=cargo_id)
        serializer = self.InputSerializer(cargo, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=200)