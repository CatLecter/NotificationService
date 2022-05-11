from rest_framework.generics import CreateAPIView

from manager_panel.models import Events
from .serializers import UGCEventSerializer


class UGCEventAPIView(CreateAPIView):
    queryset = Events.objects.all()
    serializer_class = UGCEventSerializer
