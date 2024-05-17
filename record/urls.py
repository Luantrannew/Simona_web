from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('customer/', views.customer_list,name = 'customer_list'),
    path('product/', views.product_list,name = 'product_list'),
    path('OrderFromCustomer/',views.order_from_customer , name = 'order_from_customer'),
    path('orderline/',views.order_line , name = 'order_line'),

    path('customer/<str:pk>',views.customer_detail, name= 'customer_detail'),
    path('order/<str:order_code>/', views.order_detail, name='order_detail'),

]

