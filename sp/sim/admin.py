# admin.py

from django.contrib import admin
from .models import GoogleOAuthSettings

@admin.register(GoogleOAuthSettings)
class GoogleOAuthSettingsAdmin(admin.ModelAdmin):
    list_display = ('client_id', 'created_at', 'updated_at')
    search_fields = ('client_id',)

# admin.py

from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from .models import UserInvitation
from django.utils.html import format_html
from django.template.loader import render_to_string
from django.utils.http import urlencode

@admin.register(UserInvitation)
class UserInvitationAdmin(admin.ModelAdmin):
    list_display = ('email', 'invited_at', 'is_registered', 'invite_link')
    search_fields = ('email',)
    actions = ['send_invitation']

    def invite_link(self, obj):
        """Generate the registration link for the invited user."""
        if obj.is_registered:
            return "Registered"
        registration_url = reverse('user_register')  # Create a URL for registration view
        return format_html('<a href="{}?token={}">Registration Link</a>', registration_url, obj.token)

    def send_invitation(self, request, queryset):
        """Send invitation email to selected users."""
        for invitation in queryset:
            registration_url = reverse('user_register')  # Adjust to your registration view
            invitation_link = f"{settings.SITE_URL}{registration_url}?token={invitation.token}"

            subject = "You're Invited to Register!"
            message = render_to_string('invitation_email.html', {'link': invitation_link})
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [invitation.email])

        self.message_user(request, "Invitations sent successfully.")

    send_invitation.short_description = "Send invitation email"
