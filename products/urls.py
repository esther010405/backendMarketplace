from django.urls import path
from .views import ProductsListCreateView, ProductDetailView, CategoryListView
app_name = 'products'
urlpatterns = [
    path('categories', CategoryListView.as_view(), name='categories'),
    path('products', ProductsListCreateView.as_view(), name='products-list-create'),
    path('products/<int:pk>', ProductDetailView.as_view(), name='product-detail'),
]