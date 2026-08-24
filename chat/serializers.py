from rest_framework import serializers
from .models import Conversation, Message
from users.serializers import UserSerializer
from products.serializers import ProductDetailSerializer

class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer pour la conversation
    """
    buyer = UserSerializer(read_only=True)
    seller = UserSerializer(read_only=True)
    product = ProductDetailSerializer(read_only=True)
    last_message =serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'product', 'buyer', 'seller', 'created_at', 'last_message']
        read_only_fields = ['id', 'created_at']

        
    def get_last_message(self, obj):
        """
        Récupération du dernier message de la conversation
        """
        last_message = obj.messages.last()
        if last_message:
            return MessageSerializer(last_message).data
        return None

class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer pour les messages
    """
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'created_at', 'is_read']
        read_only_fields = ['id','sender' , 'created_at', 'is_read']

