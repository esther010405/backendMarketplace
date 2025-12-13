from django.urls import path
from .views import  UserDetailView, UserProfileView , UserRegistrationView, CustomTokenObtainPairView, UserListView
app_name = 'users'
urlpatterns = [
    path('users/register', UserRegistrationView.as_view(), name='user-register'),
    path('users/<int:pk>', UserDetailView.as_view(), name='user-detail'),
    path('users/profile', UserProfileView.as_view(), name='user-profile'),
    path('users/login', CustomTokenObtainPairView.as_view(), name='login'),
    path('users/list', UserListView.as_view(), name='user-list'),
]   