from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title
# models.py

from django.db import models
from django.contrib.auth.models import User

class GoogleOAuthSettings(models.Model):
    client_id = models.CharField(max_length=255, help_text="Google OAuth Client ID")
    client_secret = models.CharField(max_length=255, help_text="Google OAuth Client Secret")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Google OAuth Settings ({self.client_id})"

# models.py

import uuid
from django.db import models

class UserInvitation(models.Model):
    email = models.EmailField(unique=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    invited_at = models.DateTimeField(auto_now_add=True)
    is_registered = models.BooleanField(default=False)

    def __str__(self):
        return f"Invitation for {self.email}"
