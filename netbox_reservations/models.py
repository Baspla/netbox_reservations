from tree_queries.fields import TreeNodeForeignKey
from tree_queries.models import TreeNode
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from tree_queries.query import TreeQuerySet

from netbox.models import NetBoxModel
from netbox_reservations.validators import ClaimValidator, ReservationValidator
from utilities.choices import ChoiceSet
from utilities.querysets import RestrictedQuerySet


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
    description = models.CharField(
        max_length=500,
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
    start_date = models.DateTimeField(
    )
    end_date = models.DateTimeField(
    )
    is_draft = models.BooleanField()

    clone_fields = (
        'contact', 'tenant', 'start_date', 'end_date', 'is_draft'
    )

    prerequisite_models = (
        'tenancy.Contact',
        'tenancy.Tenant',
    )

    def status(self):
        if self.is_draft:
            return 'Draft'
        elif self.start_date > timezone.now():
            return 'Planned'
        elif self.end_date < timezone.now():
            return 'Overdue'
        else:
            return 'Active'

    def clean(self):
        ReservationValidator().validate(self)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:netbox_reservations:reservation', args=[self.pk])


class ClaimQuerySet(TreeQuerySet, RestrictedQuerySet):
    def has_filters(self):
        return self._has_filters()


class Claim(NetBoxModel, TreeNode):
    reservation = models.ForeignKey(
        to=Reservation,
        on_delete=models.CASCADE,
        related_name='claims'
    )
    parent = TreeNodeForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_("parent"),
        related_name="children",
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

    clone_fields = (
        'reservation',
    )

    prerequisite_models = (
        'netbox_reservations.Reservation',
        'extras.Tag'
    )

    def clean(self):
        ClaimValidator().validate(self)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        unique_together = ('reservation', 'tag')

    class MPTTMeta:
        order_insertion_by = ('tag',)

    def __str__(self):
        return f'Claim for {self.tag} by {self.reservation}'

    def get_absolute_url(self):
        return reverse('plugins:netbox_reservations:claim', args=[self.pk])

    def get_restriction_color(self):
        return RestrictionChoices.colors.get(self.restriction)

    def get_tag_color(self):
        return self.tag.color
