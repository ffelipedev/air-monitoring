from django.urls import path
from . import views

app_name = 'airmonitoring'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/calidad-aire/', views.obtener_calidad_aire, name='api_calidad_aire'),
]