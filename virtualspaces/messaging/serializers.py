from rest_framework import serializers

from . import models


class MessageSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='message_id', read_only=True)
    sender_id = serializers.CharField(source='sender.id', read_only=True)
    sender_name = serializers.CharField(source='sender.username', read_only=True)
    thread_id = serializers.CharField(source='thread.thread_id', read_only=True)

    class Meta:
        model = models.Message
        fields = ('id', 'date', 'content', 'sender_id', 'sender_name', 'thread_id')


class MessageListSerializer(serializers.ListSerializer):
    child = MessageSerializer()
    many = True
    allow_null = True


class MessageThreadSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='thread_id', read_only=True)
    unread_count = serializers.IntegerField(read_only=True)
    last_message = MessageSerializer(read_only=True, many=False)

    class Meta:
        model = models.MessageThread
        fields = ('id', 'last_message', 'unread_count')


class MessageThreadListSerializer(serializers.ListSerializer):
    child = MessageThreadSerializer()
    many = True
    allow_null = True
