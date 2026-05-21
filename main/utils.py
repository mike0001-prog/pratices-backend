from .models import Room
from django.contrib.auth.models import User,AnonymousUser
from django.db.models import Q
from django import forms
from channels.db import database_sync_to_async 
from rest_framework.authtoken.models import Token
from urllib.parse import parse_qs


@database_sync_to_async
def get_user(token_key):
    print("getting user")
    try:
        token =  Token.objects.select_related("user").get(key=token_key)
        print(token.user)
        return token.user
    except Token.DoesNotExist:
        print("error gettting users")
        return AnonymousUser
    
class TokenAuthMiddleware:
    def __init__(self,app):
        self.app = app
    async def __call__(self, scope, recieve,send):
        headers = dict(scope.get("headers",[]))
        query_string = scope.get("query_string",b"").decode()
        query_params =  parse_qs(query_string)
        token_key =  query_params.get("token",[None])[0]
        if token_key:
            scope["user"] = await get_user(token_key)
        else:
            scope["user"] = AnonymousUser()
        # if b"authorization" in headers:
        #     print("checking authorization header")
        #     try:
        #         token_name,token_key = headers[b"authorization"].decode().split()
        #         if token_name.lower() == "token":
        #             scope["user"] = await get_user(token_key)
        #     except ValueError:
        #         pass
        # if "user" not in scope:
        #     scope["user"] = AnonymousUser()
        return await self.app(scope,recieve,send)

def get_room_ids():
    user = User.objects.get(username="luis")
    rooms = Room.objects.filter(Q(user_one=user) | Q(user_two=user)).values_list("id",flat=True)
    room_list = list(rooms)
    return rooms

# def connect_room(channel_layer,channel_name,id):
#     room_group_name = f"chat_{id}"
#     channel_layer.group_add(
#                     room_group_name,
#                     channel_name
#                 )
    
# class CustomUserCreation(UserCreationForm):
#     email = forms.EmailField()