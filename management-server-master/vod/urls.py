from django.urls import path
from .views import CreateAndListVODCategoryView, CreateAndListVODContentView

urlpatterns = [
    path('categories/', CreateAndListVODCategoryView.as_view(),
         name='create_and_list_VOD_Categories'),
    path('contents/', CreateAndListVODContentView.as_view(),
         name='create_and_list_VOD_Contents'),
]
