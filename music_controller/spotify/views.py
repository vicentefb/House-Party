from django.shortcuts import render, redirect
from .credentials import REDIRECT_URI, CLIENT_SECRET, CLIENT_ID
from  rest_framework.views import APIView
from requests import Request, post
from rest_framework import status
from rest_framework.response import Response
from .util import *
from api.models import Room
from .models import Vote

# 1. Request authorization to access data
# Authenticate application to request access with Spotify
# This endpoint will return us a url that we can go to authenticate our Spotify application
# Note: after we send the request to the URL we need a callback to take in the code 
# This endpoint will be called from the frontend
class AuthURL(APIView):
    def get(self, request, format=None):
        # scopes refers to the information we want to access to
        scopes = 'user-read-playback-state user-modify-playback-state user-read-currently-playing'
        # this is the firs url we need to hit and ask for authorization
        # params needs: client_id, response_type, redirect_uri, and scope
        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI, 
            'client_id': CLIENT_ID
        }).prepare().url

        return Response({'url':url}, status=status.HTTP_200_OK)

def spotify_callback(request, format=None):
    # We need code because it's how we are going to authenticate the user
    code = request.GET.get('code')
    error = request.GET.get('error')

    # Send the information to the Spotify servce
    # post method will send the request and we get a response and convert it to json
    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI, 
        'client_id': CLIENT_ID, 
        'client_secret': CLIENT_SECRET
    }).json()

    # We want to look at the response to get token information
    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')

    # As soon as I get access to the information from above I want to store it in database
    # Make sure we have a session key
    if not request.session.exists(request.session.session_key):
        request.session.create()

    update_or_create_user_tokens(request.session.session_key, access_token, token_type, expires_in, refresh_token)
    # we want to redirect back to the homepage
    return redirect('frontend:')


# This will tell us wheter or not we are authenticated
class IsAuthenticated(APIView):
    def get(self, request, format=None):
        is_authenticated = is_spotify_authenticated(self.request.session.session_key)
        return Response({'status': is_authenticated}, status=status.HTTP_200_OK)


# View to return information about the current song
class CurrentSong(APIView):
    def get(self, request, format=None):
        room_code = self.request.session.get('room_code')
        # get access to this room object because whoever is requesting information about the current song
        # may not be the host or the person authenticated with Spotify
        room = Room.objects.filter(code=room_code)
        if room.exists():
            room = room[0]
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        # if we get the room we can get the token information
        host = room.host
        # we need to send a request to spotify and send it with our token
        endpoint = "player/currently-playing"
        response = execute_spotify_api_request(host, endpoint)
        # make sure we don't have an error
        # if this is true it means we don't have any song information at the moment
        if 'error' in response or 'item' not in response:
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        # item stores a dictionary
        item = response.get('item')
        duration = item.get('duration_ms')
        progress = response.get('progress_ms')
        album_cover = item.get('album').get('images')[0].get('url')
        is_playing = response.get('is_playing')
        song_id = item.get('id')

        # handle if we have multiple artists for a song
        artist_string = ""
        for i, artist in enumerate(item.get('artists')):
            # if it's not the first artist in the list
            if i > 0:
                artist_string += ", "
            name = artist.get('name')
            artist_string += name
        votes = len(Vote.objects.filter(room=room, song_id=song_id))
        # Custom object that has information about the song we want to send
        song = {
            'title': item.get('name'),
            'artist': artist_string,
            'duration': duration,
            'time': progress,
            'image_url': album_cover,
            'is_playing': is_playing,
            'votes': votes,
            'votes_required': room.votes_to_skip,
            'id': song_id
        }
        self.update_room_song(room, song_id)

        return Response(song, status=status.HTTP_200_OK)

    def update_room_song(self, room, song_id):
        current_song = room

        if current_song != song_id:
            # means that our song has changed
            room.current_song = song_id
            room.save(update_fields=['current_song'])
            # delete all votes from that room
            votes = Vote.objects.filter(room=room).delete()

class PauseSong(APIView):
    # PUT request because we are updating the state of the song
    def put(self, request, format=None):
        # see if user that sends the request has permission to send the request
        room_code = self.request.session.get('room_code')
        room = Room.objects.filter(code=room_code)[0]
        if self.request.session.session_key == room.host or room.guest_can_pause:
            pause_song(room.host)
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        return Response({}, status=status.HTTP_403_FORBIDDEN)

class PlaySong(APIView):
    # PUT request because we are updating the state of the song
    def put(self, request, format=None):
        # see if user that sends the request has permission to send the request
        room_code = self.request.session.get('room_code')
        room = Room.objects.filter(code=room_code)[0]
        if self.request.session.session_key == room.host or room.guest_can_pause:
            play_song(room.host)
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        return Response({}, status=status.HTTP_403_FORBIDDEN)


class SkipSong(APIView):
    def post(self, request, format=None):
        room_code = self.request.session.get('room_code')
        room = Room.objects.filter(code=room_code)[0]
        # Get all the current votes for this song
        votes = Vote.objects.filter(room=room, song_id=room.current_song)
        votes_needed = room.votes_to_skip
        # Check if the user is host
        if self.request.session.session_key == room.host or len(votes)+1 >= votes_needed:
            # clear the votes we already have
            votes.delete()
            skip_song(room.host)
        else:
            # Creating a vote
            vote = Vote(user=self.request.session.session_key, room=room, song_id=room.current_song)
            vote.save()

        return Response({}, status.HTTP_204_NO_CONTENT)