from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Cargo


class DeleteCargoView(APIView):

    @swagger_auto_schema(responses={
        204: "Deleted",
        404: "Not found",
    }, tags=["cargo"],
    )
    def delete(self, request, cargo_id: int):
        cargo = get_object_or_404(Cargo, id=cargo_id)
        cargo.delete()
        return Response(status=204)
