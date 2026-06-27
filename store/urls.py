from django.urls import path
from . import views

# app_name = "store" 

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path("order/<int:product_id>/", views.create_order, name="create_order"),
    path("my-orders/", views.my_orders, name="my_orders"),

    path('orders', views.order_list, name='order_list'),
    path('category/<str:category>/', views.category_view, name='category_view'),
    path('search/', views.search, name='search'),
    path('old-catalog/', views.old_catalog, name='old_catalog'),
    path('category/<slug:slug>', views.category_detail, name='category_detail'),
]