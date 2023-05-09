from django.urls import path

from . import views

urlpatterns = [
    path('', views.sign_in, name='sign_in'),
    path('user', views.user_sign_in, name='user_sign_in'),
    path('logout', views.log_out, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('statistics', views.statistics, name='statistics')
]
