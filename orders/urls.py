from django.urls import path

from . import views

urlpatterns = [
    path('create_order/<room_id>', views.order, name="create_order"),
    path('list_orders', views.list_order, name="list_orders"),
    path('cancel_order', views.cancel_order, name="cancel_order"),
]
