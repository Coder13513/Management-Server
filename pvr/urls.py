from django.urls import path
from pvr.views import ListRecordingView, UpdateAndDeleteRecordingView

urlpatterns = [
    path('', ListRecordingView.as_view(), name='create_and_list_personal_Recording'),
    path('<int:id>', UpdateAndDeleteRecordingView.as_view(), name='update_remove_Recording') 
]
