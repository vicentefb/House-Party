from django.shortcuts import render
# Create class to inherti from the generics api
from rest_framework import generics
from .serializers import RoomSerializer
from .models import Room

# Create your views here.
# Create an api vew to see a list of all the different rooms
# This will allow us to create and view rooms
class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer