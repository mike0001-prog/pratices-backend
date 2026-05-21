from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
# Create your models here.
class TodoList(models.Model):
    # user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} list"
    
class TodoListItem(models.Model):
    todolist = models.ForeignKey(TodoList, on_delete=models.CASCADE)
    text = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.todolist} List Item"

class Room(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4,editable=False)
    user_one = models.ForeignKey(User,on_delete=models.CASCADE, related_name="room_user_one", null= True,default=None)
    user_two = models.ForeignKey(User,on_delete=models.CASCADE, related_name="room_user_two",null=True, default=None )
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(default=timezone.now())
    # last_message = models.TextField()
    # title = models.CharField(default="none", max_length=100)

    def __str__(self):
        return f"{self.user_one} X {self.user_two}"

    class Meta:
        unique_together = ("user_one","user_two",)
class Message(models.Model):
    room = models.ForeignKey(Room,on_delete=models.CASCADE)
    content = models.TextField()
    sender = models.ForeignKey(User,on_delete=models.CASCADE,null=True, default=None )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"#{self.room.id} sender {self.sender}"

