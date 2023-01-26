from django.urls import path

from netbox.views.generic import ObjectChangeLogView
from . import models, views


urlpatterns = (

    path('workspaces/', views.WorkspaceListView.as_view(), name='workspace_list'),
    path('workspaces/add/', views.WorkspaceEditView.as_view(), name='workspace_add'),
    path('workspaces/<int:pk>/', views.WorkspaceView.as_view(), name='workspace'),
    path('workspaces/<int:pk>/edit/', views.WorkspaceEditView.as_view(), name='workspace_edit'),
    path('workspaces/<int:pk>/delete/', views.WorkspaceDeleteView.as_view(), name='workspace_delete'),
    path('workspaces/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='workspace_changelog', kwargs={
        'model': models.Workspace
    }),
)
