from django.contrib import admin
from .models import Category, Product, Type


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug','image','description']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)

class TypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug','category']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Type, TypeAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'product_type', 'category','price', 'stock', 'available', 'created', 'updated','pair']
    list_filter = ['available', 'created', 'updated', 'product_type']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',),}
admin.site.register(Product, ProductAdmin)
