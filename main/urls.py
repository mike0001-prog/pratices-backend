# from django.contrib import admin
from django.urls import path
from .views import (TodoListAPIView,
create_todo_list_item, RoomCreateList,register,login,getusers,changepassword,
TodoListUpdateDestroy,TodoListItemUpdateDestroy,create_get_messages,updateusername,user_profile)
from rest_framework.authtoken.views import obtain_auth_token
# from 
urlpatterns = [
    # path('admin/', admin.site.urls),
    path("create_list/", TodoListAPIView.as_view()),
    path("create_item/<int:id>/", create_todo_list_item),
    path("login/", login),
    path("update_delete_list/<int:pk>/", TodoListUpdateDestroy.as_view()),
    # path("get_todo_item/<int:id>/",TodoListItemList.as_view())
    path("update_delete_item/<int:pk>/", TodoListItemUpdateDestroy.as_view()),
    path("rooms/", RoomCreateList.as_view()),
    path("signup/", register),
    path("room/<str:roomId>/messages/",create_get_messages),
    path("users/", getusers),
    path("user/change_username/",updateusername),
    path("user/change_password/", changepassword),
    path("user/profile/", user_profile),
    # path("voice_speech/", test_voices_speech ),

]