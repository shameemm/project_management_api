# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.user = self.scope.get('user', AnonymousUser())
            
            # Ensure the user is authenticated
            if self.user.is_authenticated:
                self.group_name = f'user_{self.user.id}'
                print(f"Connecting user: {self.user.id}, group: {self.group_name}")

                # Join the group
                await self.channel_layer.group_add(
                    self.group_name,
                    self.channel_name
                )
                await self.accept()
            else:
                print("User is not authenticated.")
                await self.close()
        except AttributeError as e:
            print(f"AttributeError in connect: {e}")
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            print(f"Disconnecting user from group: {self.group_name}")
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
        else:
            print("group_name not set during disconnect.")

    async def receive(self, text_data):
        # Handle incoming messages if needed
        pass

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            'message': event.get('message', ''),
            'user': event.get('user', '')
        }))
