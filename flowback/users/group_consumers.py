
# chat/group_consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from flowback.users.models import User, GroupChatMessage
from flowback.users.serializer import GetGroupChatMessagesSerializer


class GroupChatConsumer(WebsocketConsumer):

    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    def save_message(self, message_details):
        try:
            logged_in_user = self.get_user(message_details['logged_in_user_id'])
            # friend = self.get_user(message_details['friend_user_id'])
            message_instance = GroupChatMessage.objects.create(group=message_details['group_id'], sender=logged_in_user,
                                                               message=message_details['message'])
            message_instance.seen_by.add(logged_in_user)
            message_instance.save()

            serializer = GetGroupChatMessagesSerializer(message_instance)
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
        message = text_data_json['message']
        print("receive", message)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        print("Chat_message", message)
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))