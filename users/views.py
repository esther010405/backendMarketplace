from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework import generics,serializers
from .models import CustomUser
from .serializers import  UserRegisterSerializer, UserSerializer as CustomUserSerializer
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



# Create your views here.
class UserRegistrationView(generics.CreateAPIView):
    """
    POST /api/users/register/
    Inscription d'un nouvel utilisateur (ouvert à tous)
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]  # Autoriser l'accès sans authentification

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    GET /api/users/profile/
    PUT /api/users/profile/
    Récupération et mise à jour du profil utilisateur (authentifié uniquement)
    """
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserListView(generics.ListAPIView):
    """
    GET /api/users/list
    Récupération de la liste des utilisateurs user.is_seller=True (authentifié uniquement)
    """
    queryset = CustomUser.objects.filter(is_seller=True)
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]  # Ouvert à tous


class UserDetailView(generics.RetrieveAPIView):
    """
    GET /api/users/<int:pk>/
    Récupération des détails d'un utilisateur par son ID (authentifié uniquement)
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]  # Ouvert à tous

class CostumTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer personnalisé pour ajouter des infos utilisateur au token
    """
    username_field = CustomUser.USERNAME_FIELD  # 'email'


    def validate(self, attrs):
        """
        Vérifie que l'utilisateur existe
        """
        email = attrs.get('email')
        password = attrs.get('password')
        print(f"🔍 Email reçu: {email}")
        print(f"🔍 Password reçu: {password}")
        try:
            user = CustomUser.objects.get(email=email)
            print(f"🔍 User trouvé: {user}")
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Utilisateur introuvable")
        
       
        # Vérifie que l'utilisateur est activé
        if not user.is_active:
            raise serializers.ValidationError("Ce compte est désactivé")
        # Vérifie le mot de passe
        if not user.check_password(password):
            print(f"🔍 Mot de passe correct est {user.password}")
            raise serializers.ValidationError("Mot de passe incorrect")
           
        
        
        refresh = self.get_token(user)
    
        
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_seller': user.is_seller,
                'city': user.city,
                'image': user.image.url if user.image else None,
                'phone_number': user.phone_number,
            }
        }
        return data
    
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    POST /api/users/login/
    Connexion avec email + password, retourne access token + refresh token + infos user
    """
    serializer_class = CostumTokenObtainPairSerializer