from django.contrib import admin

from . import models


class MessageInline(admin.TabularInline):
    model = models.Message


@admin.register(models.MessageThread)
class MessageThreadAdmin(admin.ModelAdmin):
    inlines = [MessageInline]
