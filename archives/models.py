from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from django.core.serializers.json import DjangoJSONEncoder
from utils.models import BaseAbstractModel
from utils.managers import CustomQuerySet, ChannelsQuery
from authentication.models import User
from liveTv.models import Channels


class Archives(BaseAbstractModel):
    """This class defines the Categories model"""

    VIDEO_TYPE = (
        ('VD', 'video_on_demand'),
        ('AR', 'archive')
    )

    name = models.CharField(max_length=255)
    channel = models.ForeignKey(Channels, on_delete=models.CASCADE)
    video_url = models.URLField(max_length=255)
    logo_image = models.FileField(blank=True, null=True)
    num_of_days = models.IntegerField(default=1)
    # video_type = models.CharField(
    #     verbose_name='video type', max_length=20, choices=VIDEO_TYPE
    # )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = models.Manager()
    active_objects = ChannelsQuery.as_manager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Saves all the changes of the Archive model"""
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Archieves"
