import os
from uuid import uuid4

from django.db import models
from django.conf import settings


class Space(models.Model):
    NOT_SUBMITTED = 0
    PENDING = 1
    APPROVED = 2
    STATUS_CHOICES = (
        (NOT_SUBMITTED, "Not Submitted"),
        (PENDING, "Awaiting Listing Approval"),
        (APPROVED, "Listing Approved")
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    title = models.CharField(max_length=150, null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    capacity = models.IntegerField(null=True, blank=True)
    hourly_rate = models.IntegerField(null=True, blank=True)
    daily_rate = models.IntegerField(null=True, blank=True)
    min_booking_hours = models.IntegerField(null=True, blank=True)
    is_hidden = models.BooleanField(default=False)
    status = models.IntegerField(choices=STATUS_CHOICES, default=NOT_SUBMITTED)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def get_space_image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join("space_{}".format(instance.space.id), filename)


class SpaceImage(models.Model):
    space = models.ForeignKey(Space, related_name='space_images', on_delete=models.CASCADE)
    original_image = models.ImageField(upload_to=get_space_image_upload_path)
    description = models.TextField(null=True, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        if self.pk:
            old = SpaceImage.objects.get(pk=self.pk)
            storage, original_name = old.original_image.storage, old.original_image.original_name
            super(SpaceImage, self).save(*args, **kwargs)
            new_name = self.original_image.name
            if new_name != original_name:
                storage.delete(original_name)
        else:
            super(SpaceImage, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.original_image.storage.delete(self.original_image.name)
        super(SpaceImage, self).delete(*args, **kwargs)
