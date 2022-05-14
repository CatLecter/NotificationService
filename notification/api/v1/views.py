from manager_panel.models import Events
from rest_framework.generics import CreateAPIView

from .serializers import UGCEventSerializer


class UGCEventAPIView(CreateAPIView):
    queryset = Events.objects.all()
    serializer_class = UGCEventSerializer
