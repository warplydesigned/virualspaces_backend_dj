import os
from uuid import uuid4

from django.db import models
from django.conf import settings
from django.utils import timezone


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

    def book_space(self, details):
        booking = SpaceBooking()
        success = booking.setup_booking(details)


def get_space_image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join("space_{}".format(instance.space.id), filename)


class SpaceImage(models.Model):
    space = models.ForeignKey(Space, related_name='space_images', on_delete=models.CASCADE)
    original_image = models.ImageField(upload_to=get_space_image_upload_path)
    description = models.TextField(null=True, blank=True)
    order = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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


class SpaceBooking(models.Model):
    PENDING = 0
    ACCEPTED = 1
    REJECTED = 2
    CANCELED = 3
    STATUS_CHOICES = (
        (PENDING, "Pending Request"),
        (ACCEPTED, "Accepted Request"),
        (REJECTED, "Rejected Request"),
        (CANCELED, "Canceled Request")
    )

    class Details:
        requested_by_id = None
        guests = None
        rate = None
        from_date = None
        to_date = None
        requested_by = None
        full_day = None
        comments = None

    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)
    full_day = models.BooleanField(default=False)
    from_date = models.DateTimeField(default=timezone.now)
    to_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    guests = models.IntegerField()
    rate = models.IntegerField()
    comments = models.TextField(null=True, blank=True)
    total = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def setup_booking(self, details):
        for key in details:
            if details[key] is not None:
                setattr(self, key, details[key])
