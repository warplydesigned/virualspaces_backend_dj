"""
virtualspaces URL Configuration for API
"""
from django.urls import path, include

# from rest_framework import routers

from virtualspaces.core import urls as core_urls
from virtualspaces.account import urls as account_urls
from virtualspaces.otp import urls as otp_urls


urlpatterns = [
    path('', include(core_urls)),
    path('api', include(account_urls)),
    path('api', include(otp_urls)),
]
