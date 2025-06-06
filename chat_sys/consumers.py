'''
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Message
from django.utils import timezone

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if not self.scope["user"].is_authenticated:
            await self.close()
            return

        self.user = self.scope["user"]
        self.other_user_id = self.scope['url_route']['kwargs']['other_user_id']
        
        # Create consistent room name
        user_ids = sorted([str(self.user.id), str(self.other_user_id)])
        self.room_name = f"chat_{user_ids[0]}_{user_ids[1]}"
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Mark unread messages as read
        await self.mark_messages_as_read()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_type = data.get('type')

            if message_type == 'chat_message':
                message = data['message'].strip()
                if not message:
                    return

                receiver = await self.get_receiver()
                if not receiver:
                    return
                
                msg_obj = await self.save_message(receiver, message)
                
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'sender_id': str(self.user.id),
                        'username': self.user.username,
                        'timestamp': msg_obj.timestamp.strftime("%I:%M %p"),
                        'message_id': str(msg_obj.id)
                    }
                )

            elif message_type == 'typing':
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'typing',
                        'user_id': str(self.user.id),
                        'username': self.user.username,
                        'is_typing': data['is_typing']
                    }
                )

            elif message_type == 'read_receipt':
                await self.mark_message_as_read(data['message_id'])

        except Exception as e:
            print(f"Error: {str(e)}")

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def typing(self, event):
        if str(self.user.id) != event['user_id']:
            await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def get_receiver(self):
        try:
            return User.objects.get(id=self.other_user_id)
        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def save_message(self, receiver, text):
        return Message.objects.create(
            sender=self.user,
            receiver=receiver,
            text=text
        )

    @database_sync_to_async
    def mark_messages_as_read(self):
        Message.objects.filter(
            receiver=self.user,
            sender_id=self.other_user_id,
            is_read=False
        ).update(is_read=True)

    @database_sync_to_async
    def mark_message_as_read(self, message_id):
        Message.objects.filter(
            id=message_id,
            receiver=self.user
        ).update(is_read=True)
'''
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Message
from django.utils import timezone
import logging
# In your chat_sys/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from newsfeed.models import Notification
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        if self.user.is_anonymous:
            await self.close()
        else:
            self.room_group_name = f'user_{self.user.id}'
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

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')
        
        if message_type == 'new_message':
            # Handle new message notification
            recipient_id = data.get('recipient_id')
            await self.channel_layer.group_send(
                f'user_{recipient_id}',
                {
                    'type': 'chat_message',
                    'message': data.get('message'),
                    'sender_id': self.user.id
                }
            )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'new_message',
            'sender_id': event['sender_id'],
            'message': event['message']
        }))

logger = logging.getLogger(__name__)
User = get_user_model()
class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            self.user = self.scope["user"]
            self.notification_group_name = f'notifications_{self.user.id}'
            
            await self.channel_layer.group_add(
                self.notification_group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'notification_group_name'):
            await self.channel_layer.group_discard(
                self.notification_group_name,
                self.channel_name
            )

    async def send_notification(self, event):
        await self.send(text_data=json.dumps(event))
        
    async def new_message(self, event):
        # Send notification about new message
        await self.send(text_data=json.dumps({
            'type': 'new_message',
            'sender_id': event['sender_id'],
            'message': event['message']
        }))
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        
    async def disconnect(self, close_code):
        pass
        
    async def receive(self, text_data):
        await self.send(text_data=f"Echo: {text_data}")
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if not self.scope["user"].is_authenticated:
            await self.close()
            return

        self.user = self.scope["user"]
        self.other_user_id = self.scope['url_route']['kwargs']['other_user_id']
        
        # Create consistent room name (fixed the double 'chat_' prefix)
        user_ids = sorted([str(self.user.id), str(self.other_user_id)])
        self.room_group_name = f"chat_{user_ids[0]}_{user_ids[1]}"
        logger.info(f"User {self.user.id} connecting to room {self.room_group_name}")

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Mark unread messages as read
        await self.mark_messages_as_read()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            logger.info(f"User {self.user.id} disconnecting from room {self.room_group_name}")
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_type = data.get('type')

            if message_type == 'chat_message':
                message = data['message'].strip()
                if not message:
                    return

                receiver = await self.get_receiver()
                if not receiver:
                    logger.error(f"Receiver {self.other_user_id} not found")
                    return
                
                msg_obj = await self.save_message(receiver, message)
                logger.info(f"Message saved: {msg_obj.id}")
                
                # Broadcast to room group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message,
                        'sender_id': str(self.user.id),
                        'username': self.user.username,
                        'timestamp': msg_obj.timestamp.strftime("%I:%M %p"),
                        'message_id': str(msg_obj.id)
                    }
                )

            elif message_type == 'typing':
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'typing',
                        'user_id': str(self.user.id),
                        'username': self.user.username,
                        'is_typing': data['is_typing']
                    }
                )

            elif message_type == 'read_receipt':
                await self.mark_message_as_read(data['message_id'])

        except Exception as e:
            logger.error(f"Error in receive: {str(e)}")
    
    async def chat_message(self, event):
        try:
            await self.send(text_data=json.dumps(event))
            logger.debug(f"Message sent to {self.channel_name}")
        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")
    
    

    async def typing(self, event):
        if str(self.user.id) != event['user_id']:
            await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def get_receiver(self):
        try:
            return User.objects.get(id=self.other_user_id)
        except User.DoesNotExist:
            return None

    
  
    @database_sync_to_async
    def save_message(self, receiver, text):
    # Save message to database
        message_obj = Message.objects.create(
            sender=self.user,
            receiver=receiver,
            text=text
    )

    # Create notification for receiver
        Notification.objects.create(
            recipient=receiver,
            message=f"{self.user.username} USER ID: {self.user.id} sent you a new message."
    )

        return message_obj

    @database_sync_to_async
    def mark_messages_as_read(self):
        Message.objects.filter(
            receiver=self.user,
            sender_id=self.other_user_id,
            is_read=False
        ).update(is_read=True)

    @database_sync_to_async
    def mark_message_as_read(self, message_id):
        Message.objects.filter(
            id=message_id,
            receiver=self.user
        ).update(is_read=True)
