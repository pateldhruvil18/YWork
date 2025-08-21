import json
from channels.generic.websocket import AsyncWebsocketConsumer
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["chatdb"]
messages = db["messages"]

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = self.scope["url_route"]["kwargs"]["department_id"]
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data["message"]
        user = data.get("user", "Anonymous")

        # Save to MongoDB
        messages.insert_one({
            "group": self.group_name,
            "user": user,
            "message": message
        })

        # Broadcast
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat_message",
                "message": message,
                "user": user
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "user": event["user"],
            "message": event["message"]
        }))
