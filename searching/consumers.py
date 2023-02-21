from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from rest_framework.utils import json


class SearchProgressConsumer(WebsocketConsumer):
    room_name = None
    room_group_name = None

    def connect(self):
        if self.scope['user'].is_anonymous:
            return self.disconnect(401)
        self.room_name = self.scope["user"].id
        self.room_group_name = f"search-progress-{self.room_name}"
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {
            'type': text_data_json["type"],
            'message': message
        })

    def search_progress(self, event):
        self.send(text_data=event["message"])
