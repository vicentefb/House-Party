from django.db import models
from api.models import Room

# Everytime we create a new room we need to authenticate the user and store multiple tokens
# We are going to create a database to store all of the tokens
# We need to associate the user session key with the token
# We only need token for the host of the room
# Remember to add the Spotify App the Installed Apps in settings.py inside music_controller folder
class SpotifyToken(models.Model):
    user = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    refresh_token = models.CharField(max_length=150)
    access_token = models.CharField(max_length=150)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)

# When a user votes they are voting to skip the current song
class Vote(models.Model):
    user = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    song_id = models.CharField(max_length=50)
    # ForeignKey helps us because Whenever we look at a vote we can see the room we're in 
    # and access all the information about the Room for that vote
    # on_delete means what should we do when the Room gets deleted, we will CASCADE and delete anything that was referencing this room
    room = models.ForeignKey(Room, on_delete=models.CASCADE)