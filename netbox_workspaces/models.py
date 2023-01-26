from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse

from netbox.models import NetBoxModel
from utilities.choices import ChoiceSet


class Workspace(NetBoxModel):
    name = models.CharField(
        max_length=100
    )
    description = models.CharField(
        max_length=500,
        blank=True
    )
    start_date = models.DateField(
    )
    end_date = models.DateField(
    )
    tenant = models.ForeignKey(
        to='tenancy.Tenant',
        on_delete=models.PROTECT,
        related_name='workspaces',
    )
    used_tags = models.ManyToManyField(
        to='extras.Tag',
        related_name='used_by_workspaces',
    )
    comments = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ('name','end_date',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('plugins:netbox_workspaces:workspace', args=[self.pk])
