import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import ListNode, Project
from profiles.models import Profile

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['project_slug']
        self.room_group_name = f'project_{self.room_name}'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        print('CONNECTED')
        await self.accept()
        
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

        await self.close()
        
    @sync_to_async
    def save_list_node(self, username, room):
        profile = Profile.objects.get(user__username=username)
        project = Project.objects.get(slug=room)
        new_list_node = ListNode.objects.create(profile=profile, project=project, last_action=f"Created by {username} ")
        new_list_node.save()
        print("List node saved")

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data['action']
        
        if action == 'add_list_node':
            username = data['username']
            room = data['room']

            await self.save_list_node(username, room)
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'add_list_node_type',
                    'action': action,
                    
                    'room': room,
                    'username': username,
                }
        
        )

    async def add_list_node_type(self, event):

        action = event['action']
        
        room = event['room']
        username = event['username']
        
        await self.send(text_data=json.dumps({
            'action': action,
            
            'room': room,
            'username': username,
        }))

