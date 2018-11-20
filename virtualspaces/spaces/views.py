from rest_framework import viewsets

from .serializers import SpaceSerializer
from .models import Space
from .filters import FilterSpaces


class SpaceViewset(viewsets.ModelViewSet):
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer
    filter_backends = [FilterSpaces]
