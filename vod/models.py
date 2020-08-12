from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from django.core.serializers.json import DjangoJSONEncoder
from utils.models import BaseAbstractModel
from utils.managers import CustomQuerySet, ChannelsQuery


class Category(BaseAbstractModel):
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
        verbose_name_plural = "Categories"


class Content(BaseAbstractModel):
    """This class defines the Content model"""

    name = models.CharField(max_length=255)
    category = models.ManyToManyField(
        Category, related_name='category')
    content_url = models.URLField(max_length=255)
    content_image = models.FileField(blank=True, null=True)
    is_popular = models.BooleanField(default=False)
    description = models.TextField()

    objects = models.Manager()
    active_objects = ChannelsQuery.as_manager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Saves all the changes of the Channels model"""
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Contents"
