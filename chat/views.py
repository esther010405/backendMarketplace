from django.shortcuts import render
from rest_framework import generics
from .models import Conversation, Message, Product
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

# Create your views here.
class ConversationCreateListView(generics.ListCreateAPIView):
    """
    GET /api/conversations/
    POST /api/conversations/
    Récupération de la liste des conversations ou création d'une nouvelle conversation
    """
    serializer_class = ConversationSerializer
    permission_classes = [AllowAny]  # Ouvert à tous

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(buyer=user) | Conversation.objects.filter(seller=user)    
    
    def perform_create(self, serializer):
        """Associe automatiquement le vendeur à l'utilisateur connecté"""
        user= self.request.user
        product_id = self.request.data.get('product')
        product = Product.objects.get(id=product_id)
        seller = product.seller
        buyer = user
        convo, created = Conversation.objects.get_or_create(
            product=product,
            buyer=buyer,
            seller=seller,
        )
        return convo
    

class MessageListCreateView(generics.ListCreateAPIView):
    """
    GET /api/chat/conversations/<id>/messages/ -> liste des messages
    POST /api/chat/conversations/<id>/messages/ -> envoyer un message
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        convo_id = self.kwargs['conversation_id']
        return Message.objects.filter(conversation_id=convo_id)

    def perform_create(self, serializer):
        convo_id = self.kwargs['conversation_id']
        serializer.save(
            sender=self.request.user,
            conversation_id=convo_id
        )