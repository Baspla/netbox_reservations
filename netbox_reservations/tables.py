import django_tables2 as tables

from dcim.models import Device
from netbox.tables import NetBoxTable, ChoiceFieldColumn, ColoredLabelColumn, columns
from .models import Reservation, Claim
from extras.models import Tag


class ReservationTable(NetBoxTable):
    name = tables.Column(
        linkify=True
    )
    contact = tables.Column(
        linkify=True
    )
    tenant = tables.Column(
        linkify=True
    )
    claim_count = tables.Column()
    status = tables.Column(
        order_by=('is_draft', 'start_date', 'end_date'),
    )

    class Meta(NetBoxTable.Meta):
        model = Reservation
        fields = (
            'pk', 'id', 'name', 'claim_count', 'contact', 'tenant', 'is_draft', 'status', 'start_date', 'end_date',
            'description')
        default_columns = ('name', 'contact', 'tenant', 'claim_count', 'start_date', 'end_date', 'is_draft', 'status')


class ReducedClaimTable(NetBoxTable):
    tag = ColoredLabelColumn()
    restriction = ChoiceFieldColumn()

    class Meta(NetBoxTable.Meta):
        model = Claim
        fields = (
            'pk', 'id', 'tag', 'restriction', 'description',
        )
        default_columns = (
            'id', 'tag', 'restriction',
        )


class ClaimTable(NetBoxTable):
    reservation = tables.Column(
        linkify=True
    )
    tag = ColoredLabelColumn()
    restriction = ChoiceFieldColumn()
    start_date = tables.Column(accessor='reservation.start_date')
    end_date = tables.Column(accessor='reservation.end_date')

    class Meta(NetBoxTable.Meta):
        model = Claim
        fields = (
            'pk', 'id', 'reservation', 'tag', 'restriction', 'description', 'start_date', 'end_date',
        )
        default_columns = (
            'id', 'reservation', 'tag', 'restriction', 'start_date', 'end_date',
        )


class ExtendedClaimTable(NetBoxTable):
    reservation = tables.Column(
        linkify=True
    )
    restriction = ChoiceFieldColumn()
    start_date = tables.Column(accessor='reservation.start_date')
    end_date = tables.Column(accessor='reservation.end_date')
    reservation__tenant = tables.Column(accessor='reservation.tenant', linkify=True)
    reservation__contact = tables.Column(accessor='reservation.contact', linkify=True)
    reservation__status = tables.Column(verbose_name='Status')

    class Meta(NetBoxTable.Meta):
        model = Claim
        fields = (
            'pk', 'id', 'reservation', 'reservation__tenant', 'reservation__contact', 'reservation__status', 'tag',
            'restriction', 'description', 'start_date', 'end_date',
        )
        default_columns = (
            'id', 'reservation', 'reservation__tenant', 'reservation__contact',
            'restriction', 'reservation__status', 'start_date', 'end_date',
        )


class TagOverviewTable(NetBoxTable):
    name = tables.Column(
        linkify=True
    )
    color = columns.ColorColumn()
    reservation_count = tables.Column(
        verbose_name='Reservations active now'
    )

    class Meta(NetBoxTable.Meta):
        model = Tag
        fields = ('pk', 'id', 'color', 'name', 'slug', 'description', 'reservation_count')
        default_columns = ('name', 'reservation_count')


class DeviceCollisionTable(NetBoxTable):
    class Meta(NetBoxTable.Meta):
        model = Device
        fields = ('pk', 'id', 'name', 'tags')
        default_columns = ('name', 'tags')
