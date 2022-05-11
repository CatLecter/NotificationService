from rest_framework.serializers import ModelSerializer

from manager_panel.models import Events


class UGCEventSerializer(ModelSerializer):
    class Meta:
        model = Events
        fields = "__all__"
