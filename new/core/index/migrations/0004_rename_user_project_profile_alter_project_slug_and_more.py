# Generated by Django 5.0.1 on 2024-03-04 22:08

import autoslug.fields
import index.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0003_rename_user_group_profile_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='user',
            new_name='profile',
        ),
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=index.models.Project.custom_populate_from, unique_with=['profile__user__username']),
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(default='⚡ New Project!', max_length=64),
        ),
    ]
