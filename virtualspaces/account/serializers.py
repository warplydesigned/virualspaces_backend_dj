from django.contrib.auth import authenticate, get_user_model
from django.conf import settings

from rest_framework import exceptions, serializers
from djoser.compat import get_user_email, get_user_email_field_name

from .models import Profile

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('display_name', 'profile_image', 'about')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many=False)

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            User._meta.pk.name,
            User.USERNAME_FIELD,
            'profile'
        )
        read_only_fields = (User.USERNAME_FIELD,)

    def update(self, instance, validated_data):
        email_field = get_user_email_field_name(User)
        if settings.SEND_ACTIVATION_EMAIL and email_field in validated_data:
            instance_email = get_user_email(instance)
            if instance_email != validated_data[email_field]:
                instance.is_active = False
                instance.save(update_fields=['is_active'])
        return super(UserSerializer, self).update(instance, validated_data)
