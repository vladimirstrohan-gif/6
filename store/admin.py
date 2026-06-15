from django.contrib import admin
from .models import Category,Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  list_display = ['name','slug']
  prepopulated_fields = {'slug':('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
  list_display = ['name','price','category','stock','is_available','total_price']
  list_editable = ['price','stock','is_available']
  search_fields = ['name','category__name']
  list_filter = ['category','is_available']
  ordering = ['-price']
  prepopulated_fields = {'slug':('name',)}
  




