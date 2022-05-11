from django.urls import path

from api.v1.views import *

urlpatterns = [
    path('ugc_event/', UGCEventAPIView.as_view()),
]
