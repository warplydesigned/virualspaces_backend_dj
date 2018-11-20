from rest_framework import serializers


from .models import Space, SpaceImage
from virtualspaces.account.serializers import UserSerializer


class SpaceImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = SpaceImage
        fields = '__all__'


class SpaceSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False)
    space_images = SpaceImageSerializer(many=True)

    class Meta:
        model = Space
        fields = (
            'id',
            'title',
            'summary',
            'capacity',
            'hourly_rate',
            'daily_rate',
            'min_booking_hours',
            'is_hidden',
            'get_status_display',
            'created_at',
            'updated_at',
            'owner',
            'space_images'
        )
