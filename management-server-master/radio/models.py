from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from django.core.serializers.json import DjangoJSONEncoder
from utils.models import BaseAbstractModel
from utils.managers import CustomQuerySet, ChannelsQuery

class RadioCategory(BaseAbstractModel):
    """This class defines the Categories model"""

    name = models.CharField(max_length=255)
    background_image = models.FileField(blank=True, null=True)
    is_adult = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)

    objects = models.Manager()
    active_objects = ChannelsQuery.as_manager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Saves all the changes of the Categories model"""
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Radio Categories"
        app_label = "radio"


class RadioChannel(BaseAbstractModel):
    """This class defines the Categories model"""

    name = models.CharField(max_length=255)
    category = models.ManyToManyField(RadioCategory, related_name='radio_category')
    channel_url = models.URLField(max_length=255)
    channel_image = models.FileField()
    EPG_file = models.FileField(blank=True, null=True)
    description = models.TextField()
    is_popular = models.BooleanField(default=False)

    objects = models.Manager()
    active_objects = ChannelsQuery.as_manager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Saves all the changes of the Channels model"""
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Radio Channels"
        app_label = "radio"



