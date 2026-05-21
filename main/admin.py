from django.contrib import admin
from .models import TodoListItem,TodoList,Room,Message
# Register your models here.

@admin.register(TodoList)
class TodoListAdmin(admin.ModelAdmin):
    model = TodoList

@admin.register(TodoListItem)
class TodoListItemAdmin(admin.ModelAdmin):
    model = TodoListItem

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    model = Room

@admin.register(Message)
class MessagesAdmin(admin.ModelAdmin):
    model = Message



