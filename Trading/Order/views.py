from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import Order
from .serializers import OrderSerializer
from .proecess_orders import process_order

class PlaceOrderView(CreateAPIView):
    serializer_class = OrderSerializer

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            pass
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
