from django.urls import path
from archives.views import CreateAndListArchiveView

urlpatterns = [
    path('', CreateAndListArchiveView.as_view(),
         name='create_and_list_archives'),
]