from netbox.api.routers import NetBoxRouter
from . import views


app_name = 'netbox_workspaces'

router = NetBoxRouter()
router.register('workspaces', views.WorkspaceViewSet)

urlpatterns = router.urls
