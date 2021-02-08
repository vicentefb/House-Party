from .models import SpotifyToken
from django.utils import timezone
from datetime import timedelta
from .credentials import CLIENT_ID, CLIENT_SECRET
from requests import post, put, get

BASE_URL = "https://api.spotify.com/v1/me/"

def get_user_tokens(session_id):
    user_tokens = SpotifyToken.objects.filter(user=session_id)
    if user_tokens.exists():
        return user_tokens[0]
    else:
        return None

# function to create or update tokens
def update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token):
    tokens = get_user_tokens(session_id)
    # expires_in will be a numeric value expressed in seconds and we want a time stamp
    expires_in = timezone.now() + timedelta(seconds=expires_in)
    # if we have tokens associated with the current user
    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        tokens.save(update_fields=['access_token', 'refresh_token', 'expires_in', 'token_type'])
    else:
        # We create a new token
        tokens = SpotifyToken(user=session_id, access_token=access_token, refresh_token=refresh_token, token_type=token_type, expires_in=expires_in)
        tokens.save()

def is_spotify_authenticated(session_id):
    tokens = get_user_tokens(session_id)
    if tokens:
        # IF we have a token check if it's expired so maybe we need to refresh it
        expiry = tokens.expires_in
        if expiry <= timezone.now():
            refresh_spotify_token(session_id)
        return True
    return False

# Send request to refresh token
def refresh_spotify_token(session_id):
    refresh_token = get_user_tokens(session_id).refresh_token

    # This will return us a new access token and refresh token
    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type':'refresh_token',
        'refresh_token': refresh_token, 
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')
    refresh_token = response.get('refresh_token')

    # Call our update or create user token
    update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token)

# We can use this function to send a request to any Spotify endpoint
def execute_spotify_api_request(session_id, endpoint, post_=False, put_=False):
    tokens = get_user_tokens(session_id)
    # This is how you send the correct authorization content to Spotify
    header = {'Content-Type': 'application/json', 'Authorization': "Bearer " + tokens.access_token}

    if post_:
        post(BASE_URL + endpoint, headers=header)
    if put_:
        put(BASE_URL + endpoint, headers=header)

    response = get(BASE_URL + endpoint, {}, headers=header)
    try:
        return response.json()
    except:
        return {'Error': 'Issue with request'}