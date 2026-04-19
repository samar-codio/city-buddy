from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.core.exceptions import ValidationError
 
class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # Get the email from the Google login attempt
        email = sociallogin.user.email
        
        # Only allow emails ending with @cfd.edu.pk
        if not email.endswith('@cfd.nu.edu.pk'):
            raise ValidationError("Access restricted to @cfd.edu.pk emails only.")