from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext as _

from allauth.socialaccount.models import SocialLogin
from rest_auth.registration.serializers import SocialLoginSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.conf import settings
from users.models import User

class CallbackSerializer(SocialLoginSerializer):
    state = serializers.CharField()

    def validate_state(self, value):
        """
        Checks that the state is equal to the one stored in the session.
        """
        try:
            SocialLogin.verify_and_unstash_state(
                self.context['request'],
                value,
            )
        # Allauth raises PermissionDenied if the validation fails
        except PermissionDenied:
            raise ValidationError(_('State did not match.'))
        return value


class DeleteUser(serializers.ModelSerializer):
    is_active = serializers.BooleanField()
    class Meta:
        model = User
        fields = ("is_active",)

    def update(self, instance, validated_data):
        is_active = validated_data.pop('is_active', None)
        instance.is_active = is_active is not None
        instance.save()
        return instance


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pasteles',
            'email', 
            'full_name', 
            'is_active', 
            'last_login', 
            'is_superuser', 
            'is_staff'
        )
        read_only_fields = ('email', 'last_login', 'is_superuser', 'is_staff', 'is_active')