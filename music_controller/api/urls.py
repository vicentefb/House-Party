# It's going to store all the urls local to this app
from django.urls import path
from .views import RoomView, CreateRoomView

urlpatterns = [
    path('room', RoomView.as_view()), # Whatever the url is call the main function and do whatever it says inside the main function
    path('create-room', CreateRoomView.as_view())
]