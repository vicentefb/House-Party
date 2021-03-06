from django.shortcuts import render
# Create class to inherti from the generics api. Status gives us access to HTTP status codes
from rest_framework import generics, status
from .serializers import RoomSerializer, CreateRoomSerializer, UpdateRoomSerializer
from .models import Room
from rest_framework.views import APIView
# To be able to send a custom response from our view 
from rest_framework.response import Response
from django.http import JsonResponse

# Create your views here.
# Create an api vew to see a list of all the different rooms
# This will allow us to create and view rooms
class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

# When we call this GetRoom with the GET request 
# we need to pass a parameter in the url called 'code'
# That code will be equal to the code room we want to get
class GetRoom(APIView):
    serializer_class = RoomSerializer
    lookup_url_kwarg = 'code'

    def get(self, request, format=None):
        # request.GET is giving you information about the url from the GET request
        # .get we are looking for any parameters in the url, one that matches 'code'
        code = request.GET.get(self.lookup_url_kwarg)
        # We can look for the code
        if code != None:
            # We will need to filter all of the our room objects
            # since code is unique is should give us only one value 
            room = Room.objects.filter(code=code)
            # If we do have a room we do
            if len(room) > 0:
                # We are going to serialze our first entry in the room and getting the data
                data = RoomSerializer(room[0]).data
                # room[0].host the host is going to be the session key of whoever is the ohost of the room
                # self.request.session.session_key we check the current session keys
                # if both are equal it means the user is the host and store that in a key called 'is_host'  
                data['is_host'] = self.request.session.session_key == room[0].host
                return Response(data, status=status.HTTP_200_OK)
            # in the situation len(room) is not greater than 0 meaning we don't have a room
            # return a response saying there is no room
            return Response({'Room Not Found': 'Invalid Room Code.'}, status=status.HTTP_404_NOT_FOUND)
        # In the situation we weren't given a code in the url
        return Response({'Bad Request': 'Code parameter not found in requests'}, status=status.HTTP_400_BAD_REQUEST)

# View to join a new room
# We receive a room code from React and check if it's valid
class JoinRoom(APIView):
    lookup_url_kwarg = 'code'
    # POST request
    def post(self, request, format=None):
        # First check if the user has an active session like in class CreateRoom
        if not self.request.session.exists(self.request.session.session_key):
            # Creating a session
            self.request.session.create()

        # Get the code from the POST request
        # This returns None if there's no code argument
        code = request.data.get(self.lookup_url_kwarg)
        # Let's check if we do have a code
        if code != None:
            room_result =  Room.objects.filter(code=code)
            if len(room_result) > 0:
                room = room_result[0]
                # make a note in the back-end that this user is in this room
                # it means that this user in this current session has this code
                self.request.session['room_code'] = code
                return Response({'message': 'Room Joined!'}, status=status.HTTP_200_OK)

            return Response({'Bad Request': 'Invalid Room Code'}, status=status.HTTP_400_BAD_REQUEST)

        # if they don't send a room code
        return Response({'Bad Request': 'Invalid post data, did not find a code key'}, status=status.HTTP_400_BAD_REQUEST)


# APIView let us overwrite methods
class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer

    def post(self, request, format=None):
        # We need access to the session id
        # check if the current request/user has an active session with our webserver
        if not self.request.session.exists(self.request.session.session_key):
            # Creating a session
            self.request.session.create()
        
        serializer = self.serializer_class(data=request.data)
        # This will tell us if the fields guest_can_paus and votes_to_skip are valid
        if serializer.is_valid():
            # Create a room
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            host = self.request.session.session_key
            queryset = Room.objects.filter(host=host)
            # Updating the room where the user already had an active room
            if queryset.exists():
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=['guest_can_pause', 'votes_to_skip'])
                # it means that this user in this current session has this code
                self.request.session['room_code'] = room.code
                return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
            else:
                room = Room(host=host, guest_can_pause=guest_can_pause, votes_to_skip=votes_to_skip)
                room.save()
                # it means that this user in this current session has this code
                self.request.session['room_code'] = room.code
                # Return the exact room they just created
                return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)
            
        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

class UserInRoom(APIView):
    # send a GET request to this endpoin to check if the user has an active session
    def get(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            # Creating a session
            self.request.session.create()
        
        data = {
            'code': self.request.session.get('room_code')
        }
        # JsonResponse() takes a Python dictionary and serializes and sends that to the front-end
        return JsonResponse(data, status=status.HTTP_200_OK)

# Endpoint to leave a room
# We use POST because we are going to remove information from the server
class LeaveRoom(APIView):
    def post(self, request, format=None):
        if 'room_code' in self.request.session:
            # This will remove room_code from the session
            self.request.session.pop('room_code')
            # We check if they are hosting a room, if they are we delete that room
            host_id = self.request.session.session_key
            room_results = Room.objects.filter(host=host_id)
            if len(room_results) > 0:
                room = room_results[0]
                room.delete()
        
        return Response({'Message':'Success'}, status=status.HTTP_200_OK)

# Update a room
# What information do i need to update a room: code and new information
# Number of votes required to skip and if the guest can pause and play
class UpdateRoom(APIView):
    serializer_class = UpdateRoomSerializer
    # patch stands for updating something in the server
    def patch(self,request, format=None):
        # passing data to the serializer
        if not self.request.session.exists(self.request.session.session_key):
            # Creating a session
            self.request.session.create()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            code = serializer.data.get('code')
            # We need to find the room that has the same code
            queryset = Room.objects.filter(code=code)
            if not queryset.exists():
                return Response({'msg': 'Room not found.'}, status=status.HTTP_400_NOT_FOUND)
            
            room = queryset[0]
            user_id = self.request.session.session_key
            if room.host != user_id:
                return Response({'msg': 'You are not the host of this room.'}, status=status.HTTP_403_FORBIDDEN)

            room.guest_can_pause = guest_can_pause
            room.votes_to_skip = votes_to_skip
            room.save(update_fields=['guest_can_pause', 'votes_to_skip'])
            return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
            
        return Response({'Bad Request': 'Invalid Data...'}, status=status.HTTP_400_BAD_REQUEST)