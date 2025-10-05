from django.urls import path
from . import views  # ← "from ." significa desde la misma app (myapp)

app_name = 'airmonitoring'

urlpatterns = [
    path('', views.index, name='index'),
    path('nasa-test/', views.nasa_test, name='nasa_test'),
]