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
        
        return new_list_node.id
    
    @sync_to_async
    def edit_list_node_content(self, list_node_id, content):
        list_node = ListNode.objects.get(id=list_node_id)
        list_node.content = content
        list_node.last_action = f"Edited by {list_node.profile.user.username}"
        list_node.save()
        
        return list_node.id

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data['action']
        
        if action == 'add_list_node':
            username = data['username']
            room = data['room']

            list_node_id = await self.save_list_node(username, room)
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'add_list_node_type',
                    'action': action,
                    
                    'room': room,
                    'list_node_id': list_node_id,
                    'username': username,
                })
            
        elif action == 'edit_list_node_content':
            list_node_id = data['list_node_id']
            room = data['room']
            username = data['username']
            content = data['content']
            
            await self.edit_list_node_content(list_node_id, content)

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'edit_list_node_content_type',
                    'action': action,
                    
                    'room': room,
                    'list_node_id': list_node_id,
                    'username': username,
                    'content': content,
                })

    async def add_list_node_type(self, event):
        action = event['action']
        
        room = event['room']
        list_node_id = event['list_node_id']
        username = event['username']
        
        await self.send(text_data=json.dumps({
            'action': action,
            
            'room': room,
            'list_node_id': list_node_id,
            'username': username,
        }))
        
    async def edit_list_node_content_type(self, event):
        action = event['action']
        
        list_node_id = event['list_node_id']
        room = event['room']
        username = event['username']
        content = event['content']

        await self.send(text_data=json.dumps({
            'action': action,
            
            'list_node_id': list_node_id,
            'room': room,
            'username': username,
            'content': content,    
        }))