from django.db import models
from django.urls import reverse

from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet


class RestrictionChoices(ChoiceSet):
    key = 'Claim.restriction'

    CHOICES = [
        ('EXCLUSIVE', 'Exclusive', 'orange'),
        ('SHARED', 'Shared', 'green'),
    ]


class Reservation(NetBoxModel):
    name = models.CharField(
        max_length=100
    )
    comments = models.TextField(
        blank=True
    )
    contact = models.ForeignKey(
        to='tenancy.Contact',
        on_delete=models.PROTECT,
        related_name='reservations',
    )
    tenant = models.ForeignKey(
        to='tenancy.Tenant',
        on_delete=models.PROTECT,
        related_name='reservations',
    )
    start_date = models.DateField(
    )
    end_date = models.DateField(
    )

    prerequisite_models = (
        'tenancy.Contact',
        'tenancy.Tenant',
    )
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:netbox_reservations:reservation', args=[self.pk])


class Claim(NetBoxModel):
    reservation = models.ForeignKey(
        to=Reservation,
        on_delete=models.CASCADE,
        related_name='claims'
    )
    tag = models.ForeignKey(
        to='extras.Tag',
        on_delete=models.PROTECT,
        related_name='claims',
    )
    restriction = models.CharField(
        max_length=20,
        choices=RestrictionChoices,
    )
    description = models.CharField(
        max_length=500,
        blank=True
    )

    prerequisite_models = (
        'netbox_reservations.Reservation',
        'extras.Tag'
    )

    class Meta:
        ordering = ('reservation', 'tag')
        unique_together = ('reservation', 'tag')

    def __str__(self):
        return f'{self.reservation}: Claim {self.tag}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_reservations:claim', args=[self.pk])

    def get_restriction_color(self):
        return RestrictionChoices.colors.get(self.restriction)

    def get_tag_color(self):
        return self.tag.color
