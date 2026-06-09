from django.urls import path
from . import views

urlpatterns = [
    path('',views.product_list, name='product_list'),
    path('<int:product_id>/',views.product_detail, name='product_detail'),
    path('order/<int:product_id>/',views.order_views, name='order_views'),
    path('orders',views.order_list, name='order_list'),
    path('category/<str:category>/', views.category_view, name='category_view'),
    path('search/', views.search_view, name='search_view'),
    path('old-catalog/', views.old_catalog, name='old_catalog'),
    
]