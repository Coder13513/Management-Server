import datetime
from datetime import datetime as dt
from django.utils.timezone import now

from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import (
    generics,
    status,
)
from rest_framework.parsers import (
    FormParser,
    MultiPartParser,
)
from rest_framework.permissions import (
    IsAuthenticated
)
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from radio.models import RadioCategory, RadioChannel
from radio.serializers import RadioCategorySerializer, RadioChannelSerializer

from utils.permissions import (
    CanEditCategory,
    IsClientAdmin,
    IsOwner,
    ReadOnly,
)

from authentication.renderer import UserJSONRenderer

class CreateAndListRadioChannelView(generics.ListCreateAPIView):
    """Handle requests for creation of category"""

    serializer_class = RadioChannelSerializer
    permission_classes = (IsClientAdmin | ReadOnly,)
    # parser_classes = (MultiPartParser, FormParser)
    renderer_classes = (UserJSONRenderer,)

    def get_queryset(self):
        user = self.request.user

        # when the user is not logged in, ask him to log in
        if user.is_authenticated:
            return RadioChannel.objects.all()
        else:
            return RadioChannel.objects.none()

        # when the user is logged then return all channels
        

    def create(self, request, *args, **kwargs):

        request.POST._mutable = True
        payload = request.data
        serializer = self.serializer_class(data=payload)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'data': {"radio channel": serializer.data}
        }
        return Response(response, status=status.HTTP_201_CREATED)


class CreateAndListRadioCategoryView(generics.ListCreateAPIView):
    """Handle requests for creation of category"""

    serializer_class = RadioCategorySerializer
    permission_classes = (IsClientAdmin | ReadOnly,)
    renderer_classes = (UserJSONRenderer,)

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated and user.role == 'admin':
            return RadioCategory.objects.all()

        return RadioCategory.active_objects.all_published()

    def create(self, request, *args, **kwargs):

        request.POST._mutable = True
        payload = request.data
        serializer = self.serializer_class(data=payload)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'data': {"Radio category": serializer.data}
        }
        return Response(response, status=status.HTTP_201_CREATED)
