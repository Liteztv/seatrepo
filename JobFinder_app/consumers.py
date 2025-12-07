from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.convo_id = self.scope["url_route"]["kwargs"]["convo_id"]
        self.room_group_name = f"conversation_{self.convo_id}"

        user = self.scope["user"]
        if not user.is_authenticated:
            await self.close()
            return

        convo = await self.get_conversation()
        if convo is None or (user != convo.user1 and user != convo.user2):
            await self.close()
            return

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()
        print("✅ WebSocket accepted for convo", self.convo_id)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data or "{}")
        message = data.get("message", "").strip()
        if not message:
            return

        user = self.scope["user"]
        convo = await self.get_conversation()
        if convo is None:
            return

        other = convo.user2 if convo.user1 == user else convo.user1

        msg = await self.create_message(convo, user, other, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "sender": user.username,
                "message": msg.body,
                "created_at": msg.created_at.strftime("%b %d, %H:%M"),
            },
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def get_conversation(self):
        from .models import Conversation
        try:
            return Conversation.objects.get(id=self.convo_id)
        except Conversation.DoesNotExist:
            return None

    @database_sync_to_async
    def create_message(self, convo, sender, receiver, body):
        from .models import Message
        return Message.objects.create(
            conversation=convo,
            sender=sender,
            receiver=receiver,
            subject=f"Message regarding {convo.job.title if convo.job else 'conversation'}",
            body=body,
            job=convo.job,
        )

