from django.urls import path
from weatherapp import views

app_name = "weather"

urlpatterns = [
    path('', views.home, name='home'),
]
