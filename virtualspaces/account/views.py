# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from rest_framework import views, permissions, status
from rest_framework.response import Response

from djoser.views import UserView as DjoserUserView, UserDeleteView as DjoserUserDeleteView
from djoser import serializers

from .models import CustomUser
from .serializers import UserSerializer
from virtualspaces.otp import permissions as otp_permissions


class UserView(DjoserUserView):
    """
    Uses the default Djoser view, but add the IsOtpVerified permission.
    Use this endpoint to retrieve/update user.
    """
    model = CustomUser
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, otp_permissions.IsOtpVerifed]


class UserDeleteView(DjoserUserDeleteView):
    """
    Uses the default Djoser view, but add the IsOtpVerified permission.
    Use this endpoint to remove actually authenticated user.
    """
    serializer_class = serializers.UserDeleteSerializer
    permission_classes = [permissions.IsAuthenticated, otp_permissions.IsOtpVerifed]

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserLogoutAllView(views.APIView):
    """
    Use this endpoint to log out all sessions for a given user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        user.jwt_secret = uuid.uuid4()
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
