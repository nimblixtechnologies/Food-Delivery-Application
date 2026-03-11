from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import calculate_total


class CalculateTotalAPIView(APIView):

    def post(self, request):
        result = calculate_total(request.data)

        if "error" in result:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)

        return Response(result, status=status.HTTP_200_OK)
