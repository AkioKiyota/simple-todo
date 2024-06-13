import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import ListNode, Project, Group
from profiles.models import Profile

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['project_id']
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
        project = Project.objects.get(id=room)
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
    
    @sync_to_async
    def change_list_group(self, list_node_id, target_group_id):
        list_node = ListNode.objects.get(id=list_node_id)
        group = Group.objects.get(id=target_group_id)
        list_node.group = group
        list_node.last_action = f"Moved to {group.title} by {list_node.profile.user.username}"
        list_node.save()
        
        return list_node.id
    
    @sync_to_async
    def add_group(self, username, room):
        project = Project.objects.get(id=room)
        profile = Profile.objects.get(user__username=username)
        new_group = Group.objects.create(profile=profile, project=project, title="New Group")
        new_group.save()
        
        return new_group.id
    
    @sync_to_async
    def edit_group_title(self, group_id, title):
        group = Group.objects.get(id=group_id)
        group.title = title
        group.save()
        
        return group.id
    
    @sync_to_async
    def delete_group(self, group_id):
        group = Group.objects.get(id=group_id)
        group.delete()
        
        return group.id

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

        elif action == 'change_list_group':
            list_node_id = data['list_node_id']
            target_group_id = data['target_group_id']
            room = data['room']
            username = data['username']
            
            await self.change_list_group(list_node_id, target_group_id)
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'change_list_group_type',
                    'action': action,
                    
                    'list_node_id': list_node_id,
                    'room': room,
                    'username': username,
                    'target_group_id': target_group_id,
                })

        elif action == 'add_group':
            room = data['room']
            username = data['username']
            
            new_group_id = await self.add_group(username, room)
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'add_group_type',
                    'action': action,
                    
                    'room': room,
                    'group_id': new_group_id,
                    'username': username,
                })
        
        elif action == 'edit_group_title':
            group_id = data['group_id']
            room = data['room']
            username = data['username']
            title = data['title']
            
            await self.edit_group_title(group_id, title)
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'edit_group_title_type',
                    'action': action,
                    
                    'group_id': group_id,
                    'room': room,
                    'username': username,
                    'title': title,
                })
        
        elif action == 'delete_group':
            group_id = data['group_id']
            room = data['room']
            username = data['username']
            
            await self.delete_group(group_id)
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'delete_group_type',
                    'action': action,
                    
                    'group_id': group_id,
                    'room': room,
                    'username': username,
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
    
    async def change_list_group_type(self, event):
        action = event['action']
        
        list_node_id = event['list_node_id']
        room = event['room']
        username = event['username']
        target_group_id = event['target_group_id']
        
        await self.send(text_data=json.dumps({
            'action': action,
            
            'list_node_id': list_node_id,
            'room': room,
            'username': username,
            'target_group_id': target_group_id,
        }))
        
    
    async def add_group_type(self, event):
        action = event['action']
        
        room = event['room']
        group_id = event['group_id']
        username = event['username']
        
        await self.send(text_data=json.dumps({
            'action': action,
            
            'room': room,
            'group_id': group_id,
            'username': username,
        }))
    
    async def edit_group_title_type(self, event):
        action = event['action']
        
        group_id = event['group_id']
        room = event['room']
        username = event['username']
        title = event['title']

        await self.send(text_data=json.dumps({
            'action': action,
            
            'group_id': group_id,
            'room': room,
            'username': username,
            'title': title,    
        }))
        
    async def delete_group_type(self, event):
        action = event['action']
        
        group_id = event['group_id']
        room = event['room']
        username = event['username']
        
        await self.send(text_data=json.dumps({
            'action': action,
            
            'group_id': group_id,
            'room': room,
            'username': username,
        }))