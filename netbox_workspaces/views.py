from django.db.models import Count

from netbox.views import generic
from . import forms, models, tables, filtersets


#
# Workspace views
#

class WorkspaceView(generic.ObjectView):
    queryset = models.Workspace.objects.all()
    permission_required = "netbox_workspaces.view_workspace"


class WorkspaceListView(generic.ObjectListView):
    queryset = models.Workspace.objects.all()
    table = tables.WorkspaceTable
    filterset = filtersets.WorkspaceFilterSet
    filterset_form = forms.WorkspaceFilterForm
    permission_required = "netbox_workspaces.view_workspace"


class WorkspaceEditView(generic.ObjectEditView):
    queryset = models.Workspace.objects.all()
    form = forms.WorkspaceForm
    permission_required = "netbox_workspaces.edit_workspace"


class WorkspaceDeleteView(generic.ObjectDeleteView):
    queryset = models.Workspace.objects.all()
    permission_required = "netbox_workspaces.delete_workspace"
