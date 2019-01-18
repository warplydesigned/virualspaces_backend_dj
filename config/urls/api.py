"""
virtualspaces URL Configuration for API
"""
from django.urls import path, include

from rest_framework import routers

from virtualspaces.core import urls as core_urls
from virtualspaces.account import urls as account_urls
from virtualspaces.otp import urls as otp_urls
from virtualspaces.spaces import viewsets as space_viewsets
from virtualspaces.messaging import viewsets as messaging_viewsets

router = routers.DefaultRouter()
router.register(r'spaces', space_viewsets.SpaceViewset, base_name='space')
router.register(r'threads', messaging_viewsets.MessageThreadsViewSet, base_name='thread')

urlpatterns = [
    path('', include(core_urls)),
    path('api/', include(account_urls)),
    path('api/', include(otp_urls)),
    path('api/', include(router.urls))
]
