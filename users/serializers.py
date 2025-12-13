from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer pour lire les infos d'un utilisateur
    ModelSerializer génère automatiquement les champs depuis le modèle
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'is_seller', 'city', 'image', 'phone_number']
        read_only_fields = ['id']

class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer pour l'inscription d'un nouvel utilisateur
    Inclut la gestion du mot de passe
    """
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, label="Password",min_length=8)
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, label="Confirm password", min_length=8)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'is_seller', 'city', 'image', 'phone_number', 'password', 'password2']

    def validate(self, data):
        """
        Vérifie que les deux mots de passe correspondent
        """
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return data
    
    def create(self, validated_data):
        """ Crée un nouvel utilisateur avec un mot de passe haché
        """
        validated_data.pop('password2')  # On n'a pas besoin de stocker password2
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(password=password,**validated_data)
        return user