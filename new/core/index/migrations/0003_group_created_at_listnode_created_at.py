# Generated by Django 5.0.1 on 2024-03-09 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0002_listnode_last_action'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='listnode',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]