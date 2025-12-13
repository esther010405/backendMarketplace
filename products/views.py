from django.shortcuts import render
from rest_framework import generics
from .models import Category, Product
from .serializers import CategorySerializer, ProductDetailSerializer, ProductListSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from products.permissions import IsOwnerOrReadOnly


# Create your views here.
class CategoryListView(generics.ListAPIView):
    """
    GET /api/categories/
    Récupération de la liste des catégories de produits
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]  # Ouvert à tous


class ProductsListCreateView(generics.ListCreateAPIView):
    """
    GET /api/products/
    POST /api/products/
    Récupération de la liste des produits ou création d'un nouveau produit
    """
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]  # Ouvert à tous pour la liste, mais restreint pour la création
    filter_backends = [DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter]  # Ajouter des filtres si nécessaire
     
    # Filtres possibles : ?category=1&is_sold=false&city=Paris
    filterset_fields = ['category', 'is_sold', 'city', 'seller']
    
    # Recherche : ?search=iphone
    search_fields = ['name', 'description', 'city']
    
    # Tri : ?ordering=-created_at
    ordering_fields = ['price', 'created_at']
    ordering = ['-created_at']  # Par défaut : plus récent d'abord
    
    def perform_create(self, serializer):
        """Associe automatiquement le vendeur à l'utilisateur connecté"""
        serializer.save(seller=self.request.user)

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/products/<int:pk>/
    PUT /api/products/<int:pk>/
    DELETE /api/products/<int:pk>/
    Récupération, mise à jour ou suppression d'un produit par son ID
    """
    queryset = Product.objects.select_related('seller', 'category').all()
    serializer_class = ProductDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]  # Seulement le propriétaire peut modifier/supprimer
    
    def get_serializer_class(self):
        """Utilise ProductListSerializer pour GET, ProductDetailSerializer pour PUT/PATCH"""
        if self.request.method == 'GET':
            return ProductDetailSerializer
        return ProductListSerializer