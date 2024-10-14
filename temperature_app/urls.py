from django.urls import path

from temperature_app import views

urlpatterns = [
    path('meteo/', views.temperature_here, name='temperature_here'),
    path('meteo/random', views.temperature_random, name='temperature_random'),
]
