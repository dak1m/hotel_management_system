from django.urls import path

from . import views

urlpatterns = [
    path('', views.sign_in, name='sign_in'),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('statistics', views.statistics, name='statistics')
]
