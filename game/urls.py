from django.urls import path
from .views import home

print("wach abro cv alik")


urlpatterns = [
    path('', home, name='home'),
]
