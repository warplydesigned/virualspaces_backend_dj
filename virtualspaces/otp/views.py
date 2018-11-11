import uuid

from rest_framework import views, permissions
from rest_framework.response import Response
from rest_framework import status

from django_otp import devices_for_user
from django_otp.plugins.otp_static.models import StaticToken, StaticDevice

from virtualspaces.otp import permissions as otp_permissions
from virtualspaces.otp.utils import get_custom_jwt, get_user_totp_device, get_user_static_device


class TOTPCreateView(views.APIView):
    """
    Use this endpoint to set up a new TOTP device
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        device = get_user_totp_device(user)
        if device is None:
            device = user.totpdevice_set.create(confirmed=False)
        url = device.config_url
        return Response(url, status=status.HTTP_201_CREATED)


class TOTPVerifyView(views.APIView):
    """
    Use this endpoint to verify/enable a TOTP device
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, token, format=None):
        user = request.user
        device = get_user_totp_device(user)
        if device is not None and device.verify_token(token):
            if not device.confirmed:
                device.confirmed = True
                device.save()
            token = get_custom_jwt(user, device)
            return Response({'token': token}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class TOTPDeleteView(views.APIView):
    """
    Use this endpoint to delete a TOTP device
    """
    permission_classes = [permissions.IsAuthenticated, otp_permissions.IsOtpVerifed]

    def post(self, request, format=None):
        user = request.user
        devices = devices_for_user(user)
        for device in devices:
            device.delete()
        user.jwt_secret = uuid.uuid4()
        user.save()
        token = get_custom_jwt(user, None)
        return Response({'token': token}, status=status.HTTP_200_OK)


class StaticCreateView(views.APIView):
    """
    Use this endpoint to create static recovery codes.
    """
    permission_classes = [permissions.IsAuthenticated, otp_permissions.IsOtpVerifed]
    number_of_static_tokens = 6

    def get(self, request, format=None):
        device = get_user_static_device(request.user)
        if not device:
            device = StaticDevice.objects.create(user=request.user, name='Static')

        device.token_set.all().delete()
        tokens = []
        for _ in range(self.number_of_static_tokens):
            token = StaticToken.random_token()
            device.token_set.create(token=token)
            tokens.append(token)

        return Response(tokens, status=status.HTTP_201_CREATED)


class StaticVerifyView(views.APIView):
    """
    Use this endpoint to verify a static token.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, token, format=None):
        user = request.user
        device = get_user_static_device(user)
        if device is not None and device.verify_token(token):
            token = get_custom_jwt(user, device)
            return Response({'token': token}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
