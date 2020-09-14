from rest_framework import serializers
from userprofile.models import UserFavourites

class UserFavouritesSerializer(serializers.ModelSerializer):
    """ User Favourites Serializer"""

    class Meta:
        model=UserFavourites
        fields=('__all__')


