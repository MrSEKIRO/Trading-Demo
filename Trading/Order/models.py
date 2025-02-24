from enum import Enum
import uuid
from django.db import models
from Users.models import User

class OrderStatus(Enum):
    PENDING = 0
    COMPLETED = 1

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto_symbol = models.CharField(max_length=10)
    amount = models.IntegerField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=False)