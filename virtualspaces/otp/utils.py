from calendar import timegm
from datetime import datetime

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.utils import jwt_decode_handler
from rest_framework_jwt.compat import get_username
from rest_framework_jwt.settings import api_settings

from django_otp import devices_for_user
from django_otp.models import Device
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_static.models import StaticDevice


def get_user_totp_device(user, confirmed=None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, TOTPDevice):
            return device
    return None


def get_user_static_device(user, confirmed=None):
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, StaticDevice):
            return device
    return None


def jwt_otp_payload(user, device=None):
    """
    Optionally include OTP device in JWT payload
    """
    # username_field = get_username_field()
    username = get_username(user)

    payload = {
        'user_id': user.pk,
        'username': username,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    }

    # Include original issued at time for a brand new token,
    # to allow token refresh
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )

    if api_settings.JWT_AUDIENCE is not None:
        payload['aud'] = api_settings.JWT_AUDIENCE

    if api_settings.JWT_ISSUER is not None:
        payload['iss'] = api_settings.JWT_ISSUER

    # custom additions
    is_user_and_device = user is not None and device is not None
    is_users_device = device.user_id == user.id
    is_device_confirmed = device.confirmed is True
    if is_user_and_device and is_users_device and is_device_confirmed:
        payload['otp_device_id'] = device.persistent_id
    else:
        payload['otp_device_id'] = None

    return payload


def get_custom_jwt(user, device):
    """
    Helper to generate a JWT for a validated OTP device.
    This resets the orig_iat timestamp, as we've re-validated the user.
    """
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_otp_payload(user, device)
    return jwt_encode_handler(payload)


def otp_is_verified(request):
    """
    Helper to determine if user has verified OTP.
    """
    auth = JSONWebTokenAuthentication()
    jwt_value = auth.get_jwt_value(request)
    if jwt_value is None:
        return False

    payload = jwt_decode_handler(jwt_value)
    persistent_id = payload.get('otp_device_id')

    if persistent_id:
        device = Device.from_persistent_id(persistent_id)
        if device is not None and device.user_id != request.user.id:
            return False
        # Valid device in JWT
        return True
    return False