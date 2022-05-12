from django.urls import path

from .views import UGCEventAPIView

urlpatterns = [
    path("ugc_event/", UGCEventAPIView.as_view()),
]
