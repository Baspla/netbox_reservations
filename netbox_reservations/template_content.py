from extras.plugins import PluginTemplateExtension
from .models import Claim, Reservation
from .tables import ClaimTable, ReservationTable


class DeviceClaimsExtension(PluginTemplateExtension):
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


class TagClaimsExtension(PluginTemplateExtension):
    model = 'extras.tag'

    def right_page(self):
        return self.x_page()

    def x_page(self):
        obj = self.context['object']
        claims = Claim.objects.filter(tag=obj)
        claims_table = ClaimTable(claims)
        return self.render(
            'netbox_reservations/tag_extend_claims.html',
            extra_context={
                'related_claims_table': claims_table
            }
        )

class TagReservationsExtension(PluginTemplateExtension):
    model = 'extras.tag'

    def right_page(self):
        return self.x_page()

    def x_page(self):
        obj = self.context['object']
        reservations = Reservation.objects.filter(claims__tag=obj)
        reservations_table = ReservationTable(reservations)
        return self.render(
            'netbox_reservations/tag_extend_reservations.html',
            extra_context={
                'related_reservations_table': reservations_table
            }
        )

class ContactReservationsExtension(PluginTemplateExtension):
    model = 'tenancy.contact'

    def right_page(self):
        return self.x_page()

    def x_page(self):
        obj = self.context['object']
        reservations = Reservation.objects.filter(contact=obj)
        reservations_table = ReservationTable(reservations)
        return self.render(
            'netbox_reservations/contact_extend.html',
            extra_context={
                'related_reservations_table': reservations_table
            }
        )

class TenantReservationsExtension(PluginTemplateExtension):
    model = 'tenancy.tenant'

    def left_page(self):
        return self.x_page()

    def x_page(self):
        obj = self.context['object']
        reservations = Reservation.objects.filter(tenant=obj)
        reservations_table = ReservationTable(reservations)
        return self.render(
            'netbox_reservations/tenant_extend.html',
            extra_context={
                'related_reservations_table': reservations_table
            }
        )

template_extensions = [DeviceClaimsExtension, TagClaimsExtension, TagReservationsExtension, ContactReservationsExtension, TenantReservationsExtension]
