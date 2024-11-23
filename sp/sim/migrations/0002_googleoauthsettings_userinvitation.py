# Generated by Django 5.1.3 on 2024-11-23 18:49

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sim', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleOAuthSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(help_text='Google OAuth Client ID', max_length=255)),
                ('client_secret', models.CharField(help_text='Google OAuth Client Secret', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserInvitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('token', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('invited_at', models.DateTimeField(auto_now_add=True)),
                ('is_registered', models.BooleanField(default=False)),
            ],
        ),
    ]