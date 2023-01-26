from rest_framework import serializers

from netbox.api.serializers import NetBoxModelSerializer
#from tenency.models import Tenant
from ..models import Workspace
from netbox.api.serializers.nested import NestedTagSerializer


class WorkspaceSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_workspaces-api:workspace-detail')
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    used_tags = NestedTagSerializer(many=True, required=False)
    #tenant = serializers.PrimaryKeyRelatedField(queryset=Tenant.objects.all(), required=True)
    class Meta:
        model = Workspace
        fields = [
            'id',
            'url',
            'name',
            'description',
            'start_date',
            'end_date',
            'used_tags',
            'comments',
            'tenant',
            'tags',
        ]

class NestedWorkspaceSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='plugins-api:netbox_workspaces-api:workspace-detail')

    class Meta:
        model = Workspace
        fields = ['id', 'url', 'name']
