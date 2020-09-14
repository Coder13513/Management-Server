from pvr.models import Recording
from pvr.serializers import RecordingSerializer
from rest_framework import generics, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from authentication.renderer import UserJSONRenderer
from django.core.exceptions import ObjectDoesNotExist
import traceback
import json
from authentication.models import UserProfile
from authentication.serializers import ProfileSerializer
from liveTv.models import Channels
from pvr.recorder import Recorder
from utils.util import time_diff
from datetime import datetime
from django.conf import settings

# Create your views here.
class ListRecordingView(generics.ListCreateAPIView):

    serializer_class = RecordingSerializer
    renderer_classes = (UserJSONRenderer,)
    permission_classes = [IsAuthenticated]
    profile_serializer = ProfileSerializer
    recorder = Recorder()

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Recording.objects.filter(owner=user.id)
        return Recording.objects.none()

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True      
        payload = request.data 
        try:
            payload['owner'] = request.user.id 
            payload = self.get_recording_image(payload, request) 
            payload = self.estimate_recording_time(payload, request.user)
            payload = self.start_recording(payload, request.user)
            print(payload)
            serializer = self.serializer_class(data=payload)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            response = {
                'data': {"stream": serializer.data}
            }
            return Response(response, status=status.HTTP_201_CREATED)
        except OverflowError as overflow:
            traceback.print_exc()
            response = {
                'error': 'user recording limit already exhausted'
            }
            return Response(response, status=status.HTTP_403_FORBIDDEN) 
        except:
            traceback.print_exc()
            self.reset_lapsed_time_asfailed(payload, request.user)
            response = {
                'error': 'failed to start recording'
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def reset_lapsed_time_asfailed(self, payload, user):
        userprofile = UserProfile.objects.get(user_id=user.id)
        userprofile.lapsed_recording_time -= payload['duration']
        userprofile.save()

    def get_recording_image(self, payload, request):
        channel = Channels.objects.get(pk=payload['channel_id'])
        payload['recording_image'] = request.build_absolute_uri(channel.channel_image.url)
        payload.pop('channel_id')
        return payload

    def estimate_recording_time(self, payload, user):	
        userprofile = UserProfile.objects.get(user_id=user.id)
        allowed_duration = userprofile.recording_time - userprofile.lapsed_recording_time
        if allowed_duration > 0 :
            payload['duration'] = allowed_duration
            userprofile.lapsed_recording_time += allowed_duration
            userprofile.save()
        else:
            raise OverflowError("user recording limit exhausted")
        return payload

    def start_recording(self, payload, user):
        user_email = user.email
        stream_name = user.email.replace("@","-").replace(".","-") + "-" + payload['channel_name'].replace(" ","-")
        payload['output_url'] = settings.RECORDING_BASE_URL + '/' + stream_name + '/index.m3u8' 
        resp = self.recorder.start(stream_name, user_email, payload['input_url'],payload['output_url'], payload['duration'])
        payload['recording_server_id'] = resp['data']['stream']['id']
        return payload


class UpdateAndDeleteRecordingView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = RecordingSerializer
    renderer_classes = (UserJSONRenderer,)
    permission_classes = [IsAuthenticated]
    queryset = Recording.objects.all()
    recorder = Recorder()
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        request.POST._mutable = True
        id = self.kwargs['id']
        try:
            userprofile = UserProfile.objects.get(user_id=request.user.id)
            recording = Recording.objects.get(pk=id)
            duration = time_diff(recording.created_at.replace(tzinfo=None), datetime.now())
            print(duration)
            self.stop_recording(recording.recording_server_id)
            userprofile.lapsed_recording_time += duration - recording.duration
            recording.duration = duration
            recording.save()
            userprofile.save()
            serializer = self.serializer_class(recording)
            response = {
                'data': {"stream": serializer.data }
            }
            return Response(response, status=status.HTTP_201_CREATED)
        except:
            traceback.print_exc()
            response = {
                'error': 'failed to stop recording'
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def calculate_recording_time(self, payload, user, id):
        userprofile = UserProfile.objects.get(user_id=user.id)
        recording = Recording.objects.get(pk=id)
        duration = time_diff(recording.created_at.replace(tzinfo=None), datetime.now())
        userprofile.lapsed_recording_time += duration - recording.duration 
        payload['duration'] = duration
        print(duration)  
        userprofile.save()

    def stop_recording(self, recording_id):
        self.recorder.stop(recording_id)

    def delete(self, request, *args, **kwargs):
        id = self.kwargs['id']
        try:
            delObj = Recording.objects.get(pk=id)
            serializer = self.serializer_class(delObj)            
            self.remove_recording(serializer.data, request.user)
            return self.destroy(request, *args, **kwargs)
        except ObjectDoesNotExist:
            response = {
                'error': 'resource doesn''t exist'
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        except:
            traceback.print_exc()
            response = {
                'error': 'failed to delete recording'
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def remove_recording(self, payload, user):
        removed = self.recorder.remove(payload['recording_server_id'])
        if removed == True:
            userprofile = UserProfile.objects.get(user_id=user.id)
            userprofile.lapsed_recording_time -= payload['duration']
            userprofile.save()
