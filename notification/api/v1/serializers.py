from manager_panel.models import Events
from rest_framework.serializers import ModelSerializer


class UGCEventSerializer(ModelSerializer):
    class Meta:
        model = Events
        fields = "__all__"
