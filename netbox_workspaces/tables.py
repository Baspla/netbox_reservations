import django_tables2 as tables

from netbox.tables import NetBoxTable, ChoiceFieldColumn
from .models import Workspace


class WorkspaceTable(NetBoxTable):
    name = tables.Column(
        linkify=True
    )

    class Meta(NetBoxTable.Meta):
        model = Workspace
        fields = ('pk', 'id', 'name', 'description','tenant', 'used_tags','start_date','end_date')
        default_columns = ('name','tenant', 'used_tags')
