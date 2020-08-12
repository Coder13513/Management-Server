from django.urls import path
from .views import CreateAndListHomeView

urlpatterns = [
    path('home/', CreateAndListHomeView.as_view(),
         name='create_and_list_home'),
]
