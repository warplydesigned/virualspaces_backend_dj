from django.db.models import Count, Q

from rest_framework import viewsets
from rest_framework import permissions

from virtualspaces.core.helpers.viewsets import ResultsSetPagination

from . import serializers as messages_serializers
from . import models as messages_models


class MessageThreadsViewSet(viewsets.ModelViewSet):
    pagination_class = ResultsSetPagination
    serializer_class = messages_serializers.MessageThreadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = messages_models.MessageThread.objects.filter(participants=self.request.user).annotate(
            unread_count=Count('receipts', filter=Q(receipts__recipient=self.request.user))
        )
        # filter(participants=self.request.user)
        return queryset
