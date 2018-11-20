from rest_framework import filters
from django.db.models import Q

from .models import Space


class FilterSpaces(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if request.user.is_authenticated:
            queryset = queryset.filter(Q(owner=request.user) | (Q(status=Space.APPROVED) & Q(is_hidden=False)))
        else:
            queryset = queryset.filter(Q(status=Space.APPROVED) & Q(is_hidden=False))
        return queryset