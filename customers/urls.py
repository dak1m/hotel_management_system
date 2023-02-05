from django.urls import path

from . import views

urlpatterns = [
    path('list_customers', views.list_customers, name='list_customers'),
    path('create_customer', views.create_customer, name='create_customer'),
    path('update_customer/<pk>', views.update_customer, name='update_customer'),
    path('delete_customer/<pk>', views.delete_customer, name='delete_customer'),
    path('load_to_csv', views.load_to_csv, name='export_customer')
]
