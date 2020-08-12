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
from liveTv.models import Categories,Channels
from liveTv.serializers import CategoriesSerializer, ChannelsSerializer
from utils.permissions import (
    CanEditCategory,
    IsClientAdmin,
    IsOwner,
    ReadOnly,
)

from authentication.renderer import UserJSONRenderer

class CreateAndListCategoryView(generics.ListCreateAPIView):
    """Handle requests for creation of category"""

    serializer_class = CategoriesSerializer
    permission_classes = (IsClientAdmin | ReadOnly,)
    renderer_classes = (UserJSONRenderer,)

    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated and user.role == 'admin':
            return Categories.objects.all()

        return Categories.active_objects.all_published()

    def create(self, request, *args, **kwargs):

        request.POST._mutable = True
        payload = request.data
        serializer = self.serializer_class(data=payload)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'data': {"category": serializer.data}
        }
        return Response(response, status=status.HTTP_201_CREATED)


class CreateAndListChannelsView(generics.ListCreateAPIView):
    """Handle requests for creation of category"""

    serializer_class = ChannelsSerializer
    permission_classes = (IsClientAdmin | ReadOnly,)
    # parser_classes = (MultiPartParser, FormParser)
    renderer_classes = (UserJSONRenderer,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'is_popular']

    def get_queryset(self):
        user = self.request.user
        chfilter = self.request.query_params.get('name',None)
        # when the user is not logged in, ask him to log in
        if user.is_authenticated:
            if chfilter is not None:
                return Channels.objects.filter(name__contains=chfilter).order_by("ch_num")
            else:
                return Channels.objects.all().order_by("ch_num")
        else:
            return Channels.objects.none()

        # when the user is logged then return all channels

    def create(self, request, *args, **kwargs):

        request.POST._mutable = True
        payload = request.data
        serializer = self.serializer_class(data=payload)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'data': {"channel": serializer.data}
        }
        return Response(response, status=status.HTTP_201_CREATED)
