from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlaceOrderView

urlpatterns = [
    path("orders/", PlaceOrderView.as_view(), name="place-order"),
]