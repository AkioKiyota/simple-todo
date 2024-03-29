# Generated by Django 5.0.1 on 2024-03-09 09:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0003_group_created_at_listnode_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='title',
            field=models.CharField(default='New Group', max_length=64),
        ),
        migrations.AlterField(
            model_name='listnode',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='list_nodes', to='index.group'),
        ),
    ]
