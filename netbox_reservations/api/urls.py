from netbox.api.routers import NetBoxRouter
from . import views


app_name = 'netbox_reservations'

router = NetBoxRouter()
router.register('reservations', views.ReservationViewSet)
router.register('claims', views.ClaimViewSet)

urlpatterns = router.urls
