from django.urls import path
from .views import index

# this is used in spotify folder in views.py
app_name = 'frontend'

urlpatterns = [
    path('', index, name=''),
    path('join', index),
    path('create', index),
    path('room/<str:roomCode>', index)
]