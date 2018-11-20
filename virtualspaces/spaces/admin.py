from django.contrib import admin

from .models import Space, SpaceImage


class SpaceImagesInline(admin.StackedInline):
    model = SpaceImage


@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    inlines = [SpaceImagesInline]
