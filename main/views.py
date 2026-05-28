from django.shortcuts import render,get_object_or_404
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response 
from .models import TodoList,TodoListItem
from .serializer import (TodoListItemSerializer,TodoListSerializer,
                         MessageSerializer,RegistrationSerializer
,RoomSerializer,LoginSerializer,TokenSerializer,UpdateUsernameSerializer,
ChangePasswordSerializer,UserSerializer,TestVoiceSerializer)
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import authenticate
from rest_framework.filters import SearchFilter
from django.db.models import Q,Count
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status
from .models import Message,Room
from django.contrib.auth.models import User

class TodoListAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = TodoListSerializer
    def get_queryset(self):
        print(self.request.user)
        return TodoList.objects.all()
    
    
@api_view(["POST","GET"])
def create_todo_list_item(request,id):
    if request.method == "POST":
        print(request.data,request.POST)
        serializer = TodoListItemSerializer(data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            todolist = TodoList.objects.get(id=id)
            todolist.count+=1
            todolist.save()
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        print("get")
        queryset = TodoListItem.objects.filter(todolist=TodoList.objects.get(id=id))
        serializer = TodoListItemSerializer(queryset,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
        

    
        
class TodoListUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoListSerializer
    queryset = TodoList.objects.all()
    permission_classes = [AllowAny]
    

class TodoListItemUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoListItemSerializer
    queryset = TodoListItem.objects.all()
    permission_classes = [AllowAny]

"""
views for demo chat application
"""

class RoomCreateList(generics.ListCreateAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # try:
            # room = Room.objects.get(user=self.request.user)
            # return Message.objects.filter(room=room).select_related("room")
            return Room.objects.filter(Q(user_one=self.request.user) | Q(user_two =self.request.user) )
        # except Exception:
        #     print(f"somthing went wrong {Exception}")
        
    

# class UserCreate(generics.CreateAPIView):
#     serializer_class = RegistrationSerializer
#     queryset = User.objects.all()
#     permission_classes = [AllowAny]
@api_view(["POST"])
def register(request):
    if request.method == "POST":
        serializer = RegistrationSerializer(data=request.data)
        # form = UserCreationForm(request.data)
        # print(form.is_valid())
        if serializer.is_valid():
            user = serializer.save()
            return Response(status=status.HTTP_201_CREATED,data={"msg":"registeration sucessfully proceed to signin"})
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["POST","GET"])
@permission_classes([IsAuthenticated])
def create_get_messages(request,roomId):
    if request.method == "POST":
        serializer = MessageSerializer(data=request.data)
        room = Room.objects.get(uuid = roomId)
        if serializer.is_valid():
            serializer.save(room=room)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "GET":
        print("getting user")
        user = request.user
        print(user)
        room = get_object_or_404(Room,Q(user_one=user) | Q(user_two =user),uuid=roomId)
        print(room)
        query = Message.objects.filter(room=room).select_related("room","sender")
        serializer = MessageSerializer(query,many=True)
        print("return data")
        return Response(data=serializer.data,status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getusers(request):
    search_query = request.query_params.get("search",None)
    if not search_query:
        connected_user = (Room.objects.filter(Q(user_one=request.user) | Q(user_two=request.user))
                        .select_related("user_one","user_two")
                        .values_list("user_one","user_two"))
        print(list(connected_user))
        connected_user_list_pair = list(connected_user)
        connected_user_list = []
        for i in connected_user_list_pair:
            for j in i:
                connected_user_list.append(j)
        # if not set(connected_user_list) :
        #     connected_user_list = set(connected_user_list).append(re)        
        connected_user_list = set(connected_user_list)
        query = User.objects.exclude(id__in = connected_user_list)

    if search_query:
        query = User.objects.filter(username__icontains = search_query)
    
    serializer = UserSerializer(query,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(["POST"])
def login(request):
    if request.method == "POST":
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(request,username=username,password=password)
            if user:
                print("authenticated")
                token,created =  Token.objects.get_or_create(user=user)
                serializer = TokenSerializer(token)
                return Response(serializer.data,status=status.HTTP_200_OK)
            else:
                return Response({"msg":"username or password is incorrect"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg":"something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateusername(request):
    if request.method == "PUT":
        serializer = UpdateUsernameSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            user_exists = User.objects.filter(username__iexact = username).exists()
            print(user_exists)
            if not  user_exists:
                user = User.objects.get(username = request.user.username)
                user.username = username
                user.save()
                return Response({"msg":"username updated "},status=status.HTTP_201_CREATED)
            else:
                return Response({"msg":"username is too common "},status=status.HTTP_400_BAD_REQUEST)
    return Response({"msg":"bad request"},status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def changepassword(request):
    if request.method == "PUT":
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            form  = SetPasswordForm(user=request.user,data=serializer.validated_data)
            print(form.is_valid())
            if form.is_valid():
                user = form.save()
                # print(user.password)
            else: 
                return Response({"msg":"password fields do not match"},status=status.HTTP_400_BAD_REQUEST)
            return Response({"msg":"password changed sucessfully"},status=status.HTTP_200_OK)
    return Response({"msg":"bad request"},status=status.HTTP_400_BAD_REQUEST)
    # return Response()

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_profile(request):
    rooms_count = Room.objects.filter(Q(user_one=request.user) | Q(user_two=request.user)).aggregate(count=Count("id")) 
    # print(rooms_count)
    message_count = Message.objects.filter(sender=request.user).aggregate(count=Count("id"))
    data = {"room_count":rooms_count["count"],"message_count":message_count["count"]}
    return Response(data,status=status.HTTP_200_OK)


# def search_users(request):
#     pass


# import os
# import uuid
# import pyttsx3
# from django.conf import settings
# from django.http import JsonResponse
# @api_view(["POST"])
# def test_voices_speech(request):
#     # text = request.GET.get("text", "Hello world")
#     serializer = TestVoiceSerializer(data=request.data)    

#     text = ""
#     if serializer.is_valid():
#         print("valid")
#         text = serializer.validated_data["text"]
#     # Create engine
#     engine = pyttsx3.init()

#     engine.setProperty("rate", 145)
#     engine.setProperty("volume", 1.0)
#     filename = f"{uuid.uuid4()}.mp3"

#     # Save path
#     audio_dir = os.path.join(settings.MEDIA_ROOT, "audio")
#     os.makedirs(audio_dir, exist_ok=True)

#     filepath = os.path.join(audio_dir, filename)

   
#     engine.save_to_file(text, filepath)
#     engine.runAndWait()
#     return Response({"url":f"/media/audio/{filename}"},status=status.HTTP_200_OK)