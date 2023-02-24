from extras.plugins import PluginTemplateExtension
from .models import Claim, Reservation
from .tables import ClaimTable, ReservationTable, ExtendedClaimTable


class DeviceClaimsExtension(PluginTemplateExtension):
    model = 'dcim.device'

    def right_page(self):
        return self.x_page()

    def x_page(self):
        obj = self.context['object']
        claims = Claim.objects.filter(tag__in=obj.tags.all())
        claims_table = ExtendedClaimTable(claims)
        return self.render(
            'netbox_reservations/extend_claims.html',
            extra_context={
                'related_claims_table': claims_table
            }
        )


class TagClaimsExtension(PluginTemplateExtension):
    model = 'extras.tag'

    def full_width_page(self):
        return self.x_page()

    def x_page(self):
        obj = self.context['object']
        claims = Claim.objects.filter(tag=obj)
        claims_table = ExtendedClaimTable(claims)
        return self.render(
            'netbox_reservations/extend_claims.html',
            extra_context={
                'related_claims_table': claims_table
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
            'netbox_reservations/extend_reservations.html',
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
            'netbox_reservations/extend_reservations.html',
            extra_context={
                'related_reservations_table': reservations_table
            }
        )


class PrefixClaimsExtension(PluginTemplateExtension):
    model = 'ipam.prefix'

    def right_page(self):
        return self.x_page()

    def x_page(self):
        obj = self.context['object']
        claims = Claim.objects.filter(tag__in=obj.tags.all())
        claims_table = ExtendedClaimTable(claims)
        return self.render(
            'netbox_reservations/extend_claims.html',
            extra_context={
                'related_claims_table': claims_table
            }
        )


class VLANClaimsExtension(PluginTemplateExtension):
    model = 'ipam.vlan'

    def right_page(self):
        return self.x_page()

    def x_page(self):
        obj = self.context['object']
        claims = Claim.objects.filter(tag__in=obj.tags.all())
        claims_table = ExtendedClaimTable(claims)
        return self.render(
            'netbox_reservations/extend_claims.html',
            extra_context={
                'related_claims_table': claims_table
            }
        )


class InterfaceClaimsExtension(PluginTemplateExtension):
    model = 'dcim.interface'

    def right_page(self):
        return self.x_page()

    def x_page(self):
        obj = self.context['object']
        claims = Claim.objects.filter(tag__in=obj.tags.all())
        claims_table = ExtendedClaimTable(claims)
        return self.render(
            'netbox_reservations/extend_claims.html',
            extra_context={
                'related_claims_table': claims_table
            }
        )


class VMClaimsExtension(PluginTemplateExtension):
    model = 'virtualization.virtualmachine'

    def right_page(self):
        return self.x_page()

    def x_page(self):
        obj = self.context['object']
        claims = Claim.objects.filter(tag__in=obj.tags.all())
        claims_table = ExtendedClaimTable(claims)
        return self.render(
            'netbox_reservations/extend_claims.html',
            extra_context={
                'related_claims_table': claims_table
            }
        )


class IPAddressClaimsExtension(PluginTemplateExtension):
    model = 'ipam.ipaddress'

    def right_page(self):
        return self.x_page()

    def x_page(self):
        obj = self.context['object']
        claims = Claim.objects.filter(tag__in=obj.tags.all())
        claims_table = ExtendedClaimTable(claims)
        return self.render(
            'netbox_reservations/extend_claims.html',
            extra_context={
                'related_claims_table': claims_table
            }
        )


class SiteGroupsClaimsExtension(PluginTemplateExtension):
    model = 'dcim.sitegroup'

    def right_page(self):
        return self.x_page()

    def x_page(self):
        obj = self.context['object']
        claims = Claim.objects.filter(tag__in=obj.tags.all())
        claims_table = ExtendedClaimTable(claims)
        return self.render(
            'netbox_reservations/extend_claims.html',
            extra_context={
                'related_claims_table': claims_table
            }
        )


template_extensions = [DeviceClaimsExtension, TagClaimsExtension, ContactReservationsExtension,
                       TenantReservationsExtension, PrefixClaimsExtension, VLANClaimsExtension,
                       InterfaceClaimsExtension,
                       VMClaimsExtension, IPAddressClaimsExtension, SiteGroupsClaimsExtension]
