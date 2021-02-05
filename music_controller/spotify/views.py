from django.shortcuts import render
from .credentials import REDIRECT_URI, CLIENT_SECRET, CLIENT_ID
from  rest_framework.views import APIView
from requests import Request, post
from rest_framework import status
from rest_framework.response import Response

# 1. Request authorization to access data
# Authenticate application to request access with Spotify
# This endpoint will return us a url that we can go to authenticate our Spotify application
# Note: after we send the request to the URL we need a callback to take in the code 
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

        return Reponse({'url':url}, status=status.HTTP_200_OK)

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