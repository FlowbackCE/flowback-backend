
# chat/group_consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from flowback.users.models import FriendChatMessage, User
from flowback.users.serializer import GetChatMessagesSerializer


class FriendsChatConsumer(WebsocketConsumer):

    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    def save_message(self, message_details):
        try:
            logged_in_user = self.get_user(message_details['logged_in_user_id'])
            friend = self.get_user(message_details['friend_user_id'])
            message_instance = FriendChatMessage.objects.create(sender=logged_in_user, receiver=friend,
                                                                message=message_details['message'])
            message_instance.save()
            serializer = GetChatMessagesSerializer(message_instance)
            return serializer.data
        except Exception as e:
            print("Exception", e)
            return {}

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_details = self.save_message(text_data_json)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message_details': message_details
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message_details = event['message_details']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message_details': message_details
        }))
