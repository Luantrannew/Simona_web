from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('upload_csv/', views.upload_csv, name='upload_csv'),

    path('customer/', views.customer_list, name='customer_list'),
    path('customer/delete/<str:pk>/', views.customer_delete, name='customer_delete'),
    path('customer/<str:pk>/', views.customer_detail, name='customer_detail'),

    path('product/', views.product_list, name='product_list'),
    path('product/delete/<str:pk>/', views.product_delete, name='product_delete'),
    path('product/<str:pk>/', views.product_detail, name='product_detail'),


    path('OrderFromCustomer/', views.order_from_customer, name='order_from_customer'),
    path('order-delete/<str:pk>/', views.order_delete, name='order_delete'),
    path('order/<str:order_code>/', views.order_detail, name='order_detail'),

    
    path('create_customer/', views.create_customer, name='create_customer'),
    path('create_product/', views.create_product, name='create_product'),
    path('form/',views.form, name='form'),

    path('segment-list/', views.segment_list, name='segment_list'),
    path('create-segment/', views.create_segment, name='create_segment'),
    path('delete-segment/<str:segment_id>/', views.delete_segment, name='delete_segment'),

    


]

