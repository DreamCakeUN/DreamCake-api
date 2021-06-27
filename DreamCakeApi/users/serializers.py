from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext as _

from allauth.socialaccount.models import SocialLogin
from rest_auth.registration.serializers import SocialLoginSerializer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

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
        instance.is_active = False if is_active is None else is_active
        instance.save()
        return instance

class PublicUserDetailSerilizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('full_name','foto')
        read_only_fields = ('full_name','foto')

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
            'is_staff',
            'foto'
        )
        read_only_fields = ('email', 'last_login', 'is_superuser', 'is_staff', 'is_active', "pasteles")


class AdminUserSerializer(serializers.ModelSerializer):
     class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('last_login', 'email', 'password')


class ModeratorUserSerializer(serializers.ModelSerializer):
     class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('last_login', 'is_superuser', 'email')


class GetUserID(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email')

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2')

    def create(self, validated_data):

        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
        )

        return user

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs


