from django.db import models
from django.conf import settings
from products.models import Product
from users.models import  CustomUser

# Create your models here.
class Conversation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='conversations')
    buyer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='buying_conversations')
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='selling_conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'buyer', 'seller')

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='messages')   
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

