from django.db.models import Count

from netbox.api.viewsets import NetBoxModelViewSet

from .. import models
from .serializers import WorkspaceSerializer

class WorkspaceViewSet(NetBoxModelViewSet):
    queryset = models.Workspace.objects.all()
    serializer_class = WorkspaceSerializer
