from django.template.defaultfilters import slugify
from autoslug import AutoSlugField
from typing import Iterable

from django.contrib.auth.models import User
from profiles.models import Profile
from django.db import models

def custom_slugify(value):
    return slugify(value).replace(' ', '_')


class Project(models.Model):
    # Constant
    is_today = models.BooleanField(default=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    
    def custom_populate_from(self):
        return self.title
    
    slug = AutoSlugField(populate_from=custom_populate_from, unique_with=['profile__user__username'])
    
    # Variable
    title = models.CharField(max_length=64, default="⚡ New Project!")
    allowed_users = models.ManyToManyField(Profile, related_name='projects_allowed_in', blank=True)

    def __str__(self):
        return self.title
    
class Group(models.Model):
    # Constant
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

class ListNode(models.Model):
    # Constant
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    
    # Variable
    is_checked = models.BooleanField(default=False)
    content = models.TextField(default="Your note here.")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    

