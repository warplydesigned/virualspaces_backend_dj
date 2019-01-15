import uuid

from django.db import models
from django.conf import settings


class MessageThread(models.Model):
    """
    Container of messages between two or users
    """
    room_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    space = models.ForeignKey('spaces.Space', on_delete=models.SET_NULL, null=True, blank=True)
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL)
    last_message = models.ForeignKey(
        'messaging.Message', null=True, blank=True, on_delete=models.SET_NULL
    )

    def mark_read(self, user):
        UnreadReceipt.objects.filter(recipient=user, thread=self).delete()

    def add_message_content(self, content, sender):
        """
        Content user adds to chat.
        """
        new_message = Message(content=content, sender=sender, thread=self)
        new_message.save()
        self.last_message = new_message
        self.save()
        for participant in self.participants.exclude(id=sender.id):
            UnreadReceipt.objects.create(recipient=participant, thread=self, message=new_message)
        return new_message


class Message(models.Model):
    """
    A single message in a thread.
    """
    message_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    thread = models.ForeignKey(
        'messaging.MessageThread', on_delete=models.CASCADE, related_name='messages'
    )
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=1024)


class UnreadReceipt(models.Model):
    """
    Model for keep track of unread messages for each user in the thread.
    """
    date = models.DateTimeField(auto_now_add=True)
    message = models.ForeignKey(
        'messaging.Message', on_delete=models.CASCADE, related_name='receipts'
    )
    thread = models.ForeignKey(
        'messaging.MessageThread', on_delete=models.CASCADE, related_name='receipts'
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receipts'
    )
