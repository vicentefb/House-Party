from rest_framework import serializers
from .models import Room
# It'll take our model i.e. a Room, and will translate it to a JSON response
# It'll take all the keys that we have inside Room class and convert them to strings

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        # id is primary key, a unique integer created automatically
        fields = ('id', 'code', 'host', 'guest_can_pause', 'votes_to_skip', 'created_at')

# Defining another serializer
# We'll send a POST request to the endpoint that we set in our views.py
class CreateRoomSerializer(serializers.ModelSerializer):
    # make sure that our data/payload sent in our POST request is valid
    class Meta:
        model = Room
        # We're looking to serialize the request
        # To make sure that when we pass data to the serializer, we have the following fields
        # and that those correpsond to the ones in the Room line 17
        fields = ('guest_can_pause', 'votes_to_skip')