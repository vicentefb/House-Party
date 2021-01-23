from rest_framework import serializers
from .models import Room
# It'll take our model i.e. a Room, and will translate it to a JSON response
# It'll take all the keys that we have inside Room class and convert them to strings

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        # id is primary key, a unique integer created automatically
        fields = ('id', 'code', 'host', 'guest_can_pause', 'votes_to_skip', 'created_at')