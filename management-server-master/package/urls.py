from django.urls import path
from .views import CreateAndListPackageView

urlpatterns = [
    path('', CreateAndListPackageView.as_view(),
         name='create_and_list_Package'),
]
