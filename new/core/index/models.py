from autoslug import AutoSlugField
from typing import Iterable

from django.contrib.auth.models import User
from django.db import models


class Project(models.Model):
    # Constant
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Gonna add slug here.
    
    # Variable
    title = models.CharField(max_length=128, default="⚡ New Project!")
    allowed_users = models.ManyToManyField(User, related_name='projects_allowed_in', blank=True)

    def __str__(self):
        return self.title
    
class Group(models.Model):
    # Constant
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class ListNode(models.Model):
    # Constant
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Variable
    is_checked = models.BooleanField(default=False)
    content = models.TextField(default="Your note here.")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    

