import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ProteindataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # I wrote this code
    async def receive(self, text_data):
        text_data_json = json.loads(text_data) # text data from input box
        message = text_data_json['message']
        username = self.scope["user"] #scope contains details about the django user from which the message was typed

        #send message typed as well as the source user who typed the message.
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': str(username) + " : "+ message
            },
        )
    # end of code I wrote 


    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message

        }))

