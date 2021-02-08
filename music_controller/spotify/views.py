from django.shortcuts import render, redirect
from .credentials import REDIRECT_URI, CLIENT_SECRET, CLIENT_ID
from  rest_framework.views import APIView
from requests import Request, post
from rest_framework import status
from rest_framework.response import Response
from .util import *
from api.models import Room

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
        # if we get the host we can get the token information
        host = room.host
        # we need to send a request to spotify and send iwth it our token
        endpoint = "player/currently-playing"
        response = execute_spotify_api_request(host, endpoint)
        print(response)

        return Response(response, status=status.HTTP_200_OK)