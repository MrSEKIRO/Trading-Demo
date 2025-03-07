from datetime import datetime
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from .Services.get_crypto_price import get_crypto_price
from Users.models import User
from .models import Order, OrderStatus
from .serializers import OrderSerializer
from .Services.proecess_orders import fulfill_order

class PlaceOrderView(CreateAPIView):
    serializer_class = OrderSerializer

    def post(self, request):
        serializer = OrderSerializer(data=request.data)

        if serializer.is_valid():
            try:
                amount = request.data.get("amount") 
                crypto_symbol = request.data.get("crypto_symbol")
                userId = request.data.get("user")

                with transaction.atomic():
                    user = User.objects.select_for_update().get(id=userId)

                    price = get_crypto_price(crypto_symbol)
                    orderPrice = price * amount

                    if user.balance < orderPrice:
                        return Response({"error": "Not enough balance"}, status=status.HTTP_400_BAD_REQUEST)
                    
                    user.balance -= orderPrice

                    order = Order.objects.create(
                        user=user,
                        crypto_symbol=crypto_symbol,
                        amount=amount,
                        price=price,
                        created_at=datetime.now(),
                        status=OrderStatus.PENDING.value
                    )

                    user.save()
                    
                fulfill_order.delay(order.id, crypto_symbol, orderPrice)

                return Response({"message": "Order placed successfully"}, status=status.HTTP_201_CREATED)
            
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)