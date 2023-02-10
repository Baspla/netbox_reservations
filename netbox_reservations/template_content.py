from extras.plugins import PluginTemplateExtension
from .models import Claim
from .tables import ClaimTable


class DeviceReservationClaim(PluginTemplateExtension):
    model = 'dcim.device'

    def right_page(self):
        return self.x_page()

    def x_page(self):
        obj = self.context['object']
        claims = Claim.objects.filter(tag__in=obj.tags.all())
        claims_table = ClaimTable(claims)
        return self.render(
            'netbox_reservations/device_extend.html',
            extra_context={
                'related_claims_table': claims_table
            }
        )


template_extensions = [DeviceReservationClaim]
