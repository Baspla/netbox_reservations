from graphene import ObjectType
from netbox.graphql.types import NetBoxObjectType
from netbox.graphql.fields import ObjectField, ObjectListField
from . import filtersets, models


#
# Object types
#

class ReservationType(NetBoxObjectType):

    class Meta:
        model = models.Reservation
        fields = '__all__'
        filterset_class = filtersets.ReservationFilterSet


class ClaimType(NetBoxObjectType):

    class Meta:
        model = models.Claim
        fields = '__all__'
        filterset_class = filtersets.ClaimFilterSet


#
# Queries
#

class Query(ObjectType):
    reservation = ObjectField(ReservationType)
    reservation_list = ObjectListField(ReservationType)

    claim = ObjectField(ClaimType)
    claim_list = ObjectListField(ClaimType)


schema = Query
