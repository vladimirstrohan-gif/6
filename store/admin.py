from django.contrib import admin
from .models import Category,Product,ProductTag,Tag,Attribute, AttributeValue, ProductAttribute,Comment,Order
from django.utils.html import format_html

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['product', 'author', 'comment', 'created_at']
    search_fields = ['product__name', 'author__username', 'comment']
    list_filter = ['product', 'author']
    ordering = ['-created_at']
    list_display_links = ['comment']

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    autocomplete_fields = ('author',)
    readonly_fields = ('created_at',)


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
  list_display = ['name', 'slug']
  prepopulated_fields = {'slug': ('name',)}
  search_fields = ('name',)

class AttributeValueInline(admin.TabularInline):
  model = AttributeValue
  extra = 1
  autocomplete_fields = ('attribute',)

@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
  list_display = ['attribute', 'value']
  search_fields = ('value', 'attribute__name')

class ProductAttributeInline(admin.TabularInline):
  model = ProductAttribute
  extra = 1
  autocomplete_fields = ('attribute_value',)
  

@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
  list_display = ['product', 'attribute_value']
  search_fields = ('product__name', 'attribute_value__value')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  list_display = ['image_preview','name','slug']
  prepopulated_fields = {'slug':('name',)}

  def image_preview(self,obj):
    return format_html(
      '<img src="{}" style="width: 80px; object-fit: cover>',
      obj.image_url
      )

class ProductTagInline(admin.TabularInline):
   model = ProductTag
   extra = 1
   autocomplete_fields = ('tag',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
   prepopulated_fields={'slug':('name',)}
   search_fields = ('name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['product_name', 'customer_name', 'phone', 'quantity', 'total_price']
    search_fields = ['product_name', 'customer_name', 'phone']
    list_filter = ['product_name']
    ordering = ['-id']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
  list_display = ['image_preview','name','price','category','stock','is_available','total_price']
  list_editable = ['price','stock','is_available']
  search_fields = ['name','category__name']
  list_filter = ['category','is_available']
  ordering = ['-price']
  prepopulated_fields = {'slug':('name',)}

  inlines = [ProductTagInline,CommentInline,ProductAttributeInline]
  
  def image_preview(self,obj):
    return format_html(
      '<img src="{}" style="width: 80px; object-fit: cover>',
      obj.image_url
    )



