from django.shortcuts import render
from rest_framework import (
    generics,
    status,
)
from rest_framework.permissions import (
    IsAuthenticated
)
from rest_framework.response import Response
from authentication.renderer import UserJSONRenderer
from userprofile.serializers import UserFavouritesSerializer
from userprofile.models import UserFavourites
from django.core.exceptions import ObjectDoesNotExist
import traceback

class UserFavouritesAPIView(generics.GenericAPIView):

    serializer_class = UserFavouritesSerializer
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)

    def get(self, request):
        user = self.request.user
        try:
            fav = UserFavourites.objects.get(user_id=user.id)
            serializer = self.serializer_class(fav)
            response = {
                'data' : serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
        except:
            response = {
                'message': 'error occurred'
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):        
        user = self.request.user       
        request.data["user"] = user.id
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'message': 'favourites saved successfully'
        }
        return Response(response, status=status.HTTP_201_CREATED)

    def put(self, request):
        user = self.request.user
        try:
            fav = UserFavourites.objects.get(user_id=user.id)
            for live in request.data["live_channels"]:
                fav.live_channels.add(live)
            for radio in request.data["radio_channels"]:
                fav.radio_channels.add(radio)
            for archive in request.data["archives"]:
                fav.archives.add(archive)
            for video in request.data["vod"]:
                fav.vod.add(video)
            fav.save()
            response = {
                'message': 'favourites saved successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response(None, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def delete(self, request):
        user = self.request.user
        try:
            fav = UserFavourites.objects.get(user_id=user.id)
            for live in request.data["live_channels"]:
                fav.live_channels.remove(live)
            for radio in request.data["radio_channels"]:
                fav.radio_channels.remove(radio)
            for archive in request.data["archives"]:
                fav.archives.remove(archive)
            for video in request.data["vod"]:
                fav.vod.remove(video)
            fav.save()
            response = {
                'message': 'favourites saved successfully'
            }
            return Response(response, status=status.HTTP_200_OK)
        except:
            traceback.print_exc()
            return Response(None, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

 
    
        
