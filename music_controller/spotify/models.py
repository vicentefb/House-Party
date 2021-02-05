from django.db import models

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