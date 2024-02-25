from django.db import models


class Project (models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    allowed_users = models.ManyToManyField('auth.User', related_name='projects_allowed_in')

    def __str__(self):
        return self.title


class List (models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

class ListNode(models.Model):
    content = models.TextField(default="Your note here.")
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)



