from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import Message,Room
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from .serializer import MessageSerializer
"""
implemntation for suscribe on demand 
a room may not have been added so there is a
a fallback which is sending the message to the recievers room directly,
then the reciver may suscribe when he/she opens the chat
"""
@receiver(post_save,sender=Message)
def message_signal(sender,instance,created,**kwargs):
    if created:
               
        channel_layer = get_channel_layer()
        print("created")
        serializer = MessageSerializer(instance)
        # try:
        #         room_id = instance.room.id
        #         # print(f"chat_{room_id}")
        #         room_group_name = f"chat_{room_id}"
        #         print(f"signals {room_group_name}")
        #         async_to_sync(channel_layer.group_send)(
        #         room_group_name,
        #         {
        #             "type": "chat.message",
        #             "data": serializer.data,
        #         }
        #     )
        # except e:
        #     print(e)
        user_room = f"room_{instance.room.user_one}" 
        if instance.room.user_one == instance.sender:
            user_room = f"room_{instance.room.user_two}"
        print(instance.room.user_one,instance.room.user_two,instance.sender)    
        print(user_room) 
        async_to_sync(channel_layer.group_send)(
            user_room,
            {
                "type": "chat.message",
                "data": {"type":"suscribe_room","data":serializer.data},
            }
        )
        print(f"created message {instance.content}")


@receiver(post_save,sender=User)
def user_signal(sender,instance,created,**kwargs):
    if created:

        Room.objects.create(user_one=instance,user_two=instance)
        print("created room for user ")
# @receiver(pre_save,sender=Message)
# def create