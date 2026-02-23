from django.urls import path
from . import views

app_name = 'leave'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('requests/', views.requests, name='requests'),
    path('settings/', views.settings, name='settings'),
]
