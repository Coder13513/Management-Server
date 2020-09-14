from django.db import models
from radio.models import RadioChannel
from liveTv.models import Channels
from archives.models import Archives
from vod.models import Content
from authentication.models import User
from utils.models import BaseAbstractModel

class UserFavourites(BaseAbstractModel):
    """ This class defines user favourites channels/Radio/Archives/VOD"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    live_channels = models.ManyToManyField(Channels, related_name="live_channels", blank=True)
    radio_channels = models.ManyToManyField(RadioChannel, related_name="radio_channels", blank=True)
    archives = models.ManyToManyField(Archives, related_name="archives", blank=True)
    vod = models.ManyToManyField(Content, related_name="vod", blank=True)

    def __str__(self):
        return f'{self.user}\'s Favourites'
