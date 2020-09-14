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
from archives.models import Archives
from archives.serializers import ArchiveSerializer
from utils.permissions import (
    CanEditCategory,
    IsClientAdmin,
    IsOwner,
    ReadOnly,
    IsAdmin,
)

from authentication.renderer import UserJSONRenderer

class CreateAndListArchiveView(generics.ListCreateAPIView):
    """Handle requests for creation of category"""

    serializer_class = ArchiveSerializer
    permission_classes = (IsClientAdmin | ReadOnly,)
    renderer_classes = (UserJSONRenderer,)

    def get_queryset(self):
        user = self.request.user

        # when the user is not logged in, ask him to log in
        if user.is_authenticated:
            return Archives.objects.all()
            
        # when the user is logged then return all channels
        else:
            return Archives.objects.none()

    def create(self, request, *args, **kwargs):

        request.POST._mutable = True
        payload = request.data
        serializer = self.serializer_class(data=payload)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = {
            'data': {"archive": serializer.data}
        }
        return Response(response, status=status.HTTP_201_CREATED)

# class GetVideoOnDemand():
