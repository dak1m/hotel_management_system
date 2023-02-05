from django.urls import path

from . import views

urlpatterns = [
    path('list_rooms', views.list_rooms, name="list_rooms"),
    path('create_room', views.create_rooms, name='create_rooms'),
    path('create_room_detail/<pk>', views.create_room_detail, name='create_room_detail'),
    path('list_room_details/<room_id>', views.list_room_details, name='list_room_details'),
    path('list_room_checkins', views.list_room_checkins, name='list_room_checkins'),
    path('check_in', views.check_in, name='check_in'),
    path('list_room_checkouts', views.list_room_checkouts, name='list_room_checkouts'),
    path('check_out', views.check_out, name='check_out'),
    path('list_checkin_customers', views.list_checkin_customers, name='list_checkin_customers'),
]
