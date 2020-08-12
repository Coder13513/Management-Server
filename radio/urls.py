from django.urls import path
from radio.views import CreateAndListRadioCategoryView, CreateAndListRadioChannelView

urlpatterns = [
    path('channels/', CreateAndListRadioChannelView.as_view(),
         name='create_and_list_channels'),
    path('categories/', CreateAndListRadioCategoryView.as_view(),
         name='create_and_list_categories'),
]
