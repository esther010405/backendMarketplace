from rest_framework import serializers
from .models import Product, Category
from users.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer pour la catégorie de produit
    """
    product_count = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'slug', 'created_at', 'product_count']
        read_only_fields = ['id']

class ProductListSerializer(serializers.ModelSerializer):
    """
    Serializer pour le produit
    Inclut les informations de la catégorie et du vendeur
    """
    category_name = serializers.CharField(source='category.name', read_only=True)
    seller_name = serializers.CharField(source='seller.email', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'image', 'city', 'is_sold', 'category', 'category_name', 'seller', 'seller_name', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']




class ProductDetailSerializer(serializers.ModelSerializer):
    """
    Serializer détaillé pour le produit
    Inclut les informations complètes de la catégorie et du vendeur
    """
    category = CategorySerializer(read_only=True)
    seller = UserSerializer(read_only=True)
 # IDs pour créer/modifier un produit
    category_id = serializers.IntegerField(source='category', write_only=True, required=False)
    seller_id = serializers.IntegerField(source='seller', write_only=True, required=False)
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'image', 'city', 'is_sold', 'category', 'category_id', 'seller', 'seller_id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']