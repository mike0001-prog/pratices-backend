from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .utils import get_room_ids
from channels.db import database_sync_to_async
# from asgiref import database_sync_to_async
from django.core.cache import cache


class Chat(AsyncWebsocketConsumer):

    async def connect(self):
        print("CONNECTED", self.channel_name)
        await self.accept()
        print(self.scope["user"])
        user_room = f"room_{self.scope["user"]}"
        print(user_room)
        await self.channel_layer.group_add(
                user_room,
                self.channel_name
            )
        # connected_users_dict = {}
        # if not cache.get("connected_users")
        # cache.set("connected_users",{})
        # connected_users_dict = cache.get("connected_users")
        # connected_users_dict[user_room] = user_room
    # self.room_name = self.scope['url_route']['kwargs']['room_name']
        # self.room_group_name = f'chat_{self.room_name}'
        # print(self.room_group_name)      
        # room_ids = await self.get_rooms()
        # print(room_ids)
        # for room in room_ids:
        #     room_name = f"chat_{room}"
        #     print(f" consumer {room_name}")
        #     await self.channel_layer.group_add(
        #         room_name,
        #         self.channel_name
        #     )
    async def disconnect(self, close_code):
        await self.close()   
   
    async def receive(self, text_data):
        # print(type(text_data))
        data = json.loads(text_data)
        if data["type"] == "typing_signal":
            user_room = f"room_{data["reciever"]}"
            print(user_room)
            await self.channel_layer.group_send(
                user_room,
                    {
                "type": "typing.signal",
                "data": {"type":"typing_signal","msg":"typing"}
            }
            )
        #     self.disconnect()
       

        # print(text_data)
        print("broadcasted")
       
    async def chat_message(self, event):
        print("EVENT:", event)
        print("chatting")
        await self.send(text_data=json.dumps({
            "data": event["data"],
        }))
    # async def suscribe_room(self,event):
    #     print("EVENT:", event)
    #     print("suscribing")
    #     room_name = event["data"]["room"]
    #     await self.channel_layer.group_add(
    #             room_name,
    #             self.channel_name
    #         )
    #     await self.send(text_data=json.dumps({
    #         "data": event["data"],
    #     }))

    async def typing_signal(self,event):
        await self.send(text_data=json.dumps({
            "data": event["data"],
        }))
       
    # async def broadcast_message(self,event):
    #     print("EVENT:", event)

    #     await self.send(text_data=json.dumps({
    #         "message": event["messa"],
    #     }))
    async def dispatch(self, message):
        print("DISPATCH RECEIVED:", message)
        await super().dispatch(message)
    @database_sync_to_async
    def get_rooms(self):
        room_list =  get_room_ids()
        return room_list
   