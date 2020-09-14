from django.urls import path

from userprofile.views import UserFavouritesAPIView

urlpatterns = [
    path("favourites/", UserFavouritesAPIView.as_view(), name="favourites")
]

