from django.db import models
import string
import random
# Create your models here.
# In django instead of creating a table we create a model

# Every time we come up with a code it needs to be a random code
def generate_unique_code():
    length = 6
    # Generate random code which is k length (6) that only contains uppercase ascii string
    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=length))
        # Check if code is unique
        # Room.objects will give you all objects and you filter them by code and check if that
        # code is the same as in line 12
        # Room.objects.filter(code=code) returns a list that meet the criteria
        if Room.objects.filter(code=code).count() == 0:
            break
    
    return code

# Create the database
class Room(models.Model):
    # code will hold a bunch of characters
    code =  models.CharField(max_length=8, default=generate_unique_code, unique=True)
    # To figure out who the host is or to be able to store the host we need to use a session key
    host = models.CharField(max_length=50, unique=True)
    guest_can_pause = models.BooleanField(null=False, default=False)
    votes_to_skip = models.IntegerField(null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)