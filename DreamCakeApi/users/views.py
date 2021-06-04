from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader, Template, Context
from django.views import View
from django.http import JsonResponse
from django.utils.translation import gettext as _

from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount.providers.base import AuthAction
# from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.oauth2.views import OAuth2LoginView
from rest_auth.registration.views import SocialConnectView, SocialLoginView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status

from .serializers import CallbackSerializer, CustomUserDetailsSerializer, DeleteUser, AdminUserSerializer, GetUserID, ModeratorUserSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from users.models import User

from rest_framework import authentication
from rest_framework import permissions

# AUTENTICATION
class AdminAuthenticationPermission(permissions.BasePermission):
    ADMIN_ONLY_AUTH_CLASSES = [authentication.BasicAuthentication, authentication.SessionAuthentication]

    def has_permission(self, request, view):
        user = request.user
        if user and user.is_superuser:
            return user.is_superuser or \
                not any(isinstance(request._authenticator, x) for x in self.ADMIN_ONLY_AUTH_CLASSES) 
        return False


class ModeratorAuthenticationPermission(permissions.BasePermission):
    ADMIN_ONLY_AUTH_CLASSES = [authentication.BasicAuthentication, authentication.SessionAuthentication]

    def has_permission(self, request, view):
        user = request.user
        if user and user.is_staff:
            return user.is_staff or \
                not any(isinstance(request._authenticator, x) for x in self.ADMIN_ONLY_AUTH_CLASSES) 
        return False





# class CallbackMixin:
#     adapter_class = FacebookOAuth2Adapter
#     client_class = OAuth2Client
#     # This is our serializer from above
#     # You can omit this if you handle CSRF protection in the frontend
#     serializer_class = CallbackSerializer

#     # Not the prettiest but single source of truth
#     @property
#     def callback_url(self):
#         url = self.adapter_class(self.request).get_callback_url(
#             self.request,
#             None,
#         )
#         return url


# class CallbackCreate(CallbackMixin, SocialLoginView):
#     """
#     Logs the user in with the providers data.
#     Creates a new user account if it doesn't exist yet.
#     """


# class CallbackConnect(CallbackMixin, SocialConnectView):
#     """
#     Connects a provider's user account to the currently logged in user.
#     """

#     # You can override this method here if you don't want to
#     # receive a token. Omit it otherwise.
#     def get_response(self):
#         return Response({'detail': _('Connection completed.')})


class FacebookLogin(APIView):
    adapter_class = FacebookOAuth2Adapter
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        """
        Returns the URL to the login page of provider's authentication server.
        """
        # You should have CSRF protection enabled, see
        # https://security.stackexchange.com/a/104390 (point 3).
        # Therefore this is a POST endpoint.
        # This code is inspired by `OAuth2LoginView.dispatch`.
        adapter = self.adapter_class(request)
        provider = adapter.get_provider()
        app = provider.get_app(request)
        view = OAuth2LoginView()
        view.request = request
        view.adapter = adapter
        client = view.get_client(request, app)
        # You can modify `action` if you have more steps in your auth flow
        action = AuthAction.AUTHENTICATE
        auth_params = provider.get_auth_params(request, action)
        # You can omit this if you want to validate the state in the frontend
        client.state = SocialLogin.stash_state(request)
        url = client.get_redirect_url(adapter.authorize_url, auth_params)
        return Response({'url': url})

class GoogleLogin(APIView):
    adapter_class = GoogleOAuth2Adapter
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        """
        Returns the URL to the login page of provider's authentication server.
        """
        # You should have CSRF protection enabled, see
        # https://security.stackexchange.com/a/104390 (point 3).
        # Therefore this is a POST endpoint.
        # This code is inspired by `OAuth2LoginView.dispatch`.
        adapter = self.adapter_class(request)
        provider = adapter.get_provider()
        app = provider.get_app(request)
        view = OAuth2LoginView()
        view.request = request
        view.adapter = adapter
        client = view.get_client(request, app)
        # You can modify `action` if you have more steps in your auth flow
        action = AuthAction.AUTHENTICATE
        auth_params = provider.get_auth_params(request, action)
        # You can omit this if you want to validate the state in the frontend
        client.state = SocialLogin.stash_state(request)
        url = client.get_redirect_url(adapter.authorize_url, auth_params)
        return Response({'url': url})

class DisableAccount(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DeleteUser

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class getID(generics.RetrieveAPIView):
    queryset = User.objects.all()
    lookup_field = 'email'

    serializer_class = GetUserID
    permission_classes = [IsAuthenticated, AdminAuthenticationPermission or ModeratorAuthenticationPermission]

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminEditUser(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    lookup_field = 'pk'

    serializer_class = AdminUserSerializer
    permission_classes = [IsAuthenticated, AdminAuthenticationPermission]

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class ModEditUser(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    lookup_field = 'pk'

    serializer_class = ModeratorUserSerializer
    permission_classes = [IsAuthenticated, ModeratorAuthenticationPermission]

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


