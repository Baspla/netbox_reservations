from rest_framework import serializers

from extras.api.serializers import NestedTagSerializer
from tenancy.api.serializers import NestedTenantSerializer, NestedContactSerializer
from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from ..models import Reservation, Claim


#
# Nested serializers
#

class NestedReservationSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_reservations-api:reservation-detail'
    )

    class Meta:
        model = Reservation
        fields = ('id', 'url', 'display', 'name')


class NestedClaimSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_reservations-api:claim-detail'
    )

    class Meta:
        model = Claim
        fields = ('id', 'url', 'display', 'tag')


#
# Regular serializers
#

class ReservationSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_reservations-api:reservation-detail'
    )
    claim_count = serializers.IntegerField(read_only=True)
    contact = NestedContactSerializer()
    tenant = NestedTenantSerializer()
    start_date = serializers.DateField()
    end_date = serializers.DateField()

    class Meta:
        model = Reservation
        fields = (
            'id', 'url', 'display', 'name', 'contact', 'tenant',
            'comments', 'tags', 'custom_fields', 'created',
            'last_updated', 'claim_count', 'start_date',
            'end_date',
        )


class ClaimSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_reservations-api:claim-detail'
    )
    reservation = NestedReservationSerializer()
    tag = NestedTagSerializer()

    class Meta:
        model = Claim
        fields = (
            'id', 'url', 'display', 'reservation', 'tag', 'restriction',
            'tags', 'custom_fields', 'created',
            'last_updated',
        )
