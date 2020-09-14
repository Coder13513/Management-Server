from django.db import models
from utils.models import BaseAbstractModel
from utils.managers import CustomQuerySet
from authentication.models import User

# Create your models here.
class Recording(BaseAbstractModel):
    channel_name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    input_url = models.CharField(max_length=1000)
    output_url = models.CharField(max_length=1000)
    duration = models.IntegerField(default=0)
    recording_server_id = models.IntegerField(default=0)
    recording_image = models.URLField(blank=True, null=True)
    objects = models.Manager()
    active_objects = CustomQuerySet.as_manager()

    def __str__(self):
        self.channel_name

    def save(self, *args, **kwargs):
        """Saves all the changes of stream model"""
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Recordings"
