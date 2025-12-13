from django.contrib import admin
from .models import Category, Product

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name', 'slug')
    ordering = ('name',)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'city', 'is_sold', 'category', 'seller', 'created_at')
    search_fields = ('name', 'description', 'city')
    list_filter = ('is_sold', 'category', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

