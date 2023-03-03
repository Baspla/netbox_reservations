import logging

from django.db.models.fields import related_descriptors
from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor
from django.test import TestCase

from extras.models import Tag
from netbox_reservations.forms import ReservationForm, ClaimForm
from netbox_reservations.models import Reservation
from tenancy.models import Contact, Tenant


class ReservationFormTestCase(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(
            name='Test Contact'
        )
        self.tenant = Tenant.objects.create(
            name='Test Tenant'
        )

    def test_reservation_form(self):
        form = ReservationForm(
            data={
                'name': 'Test Reservation',
                'comments': 'Test Comments',
                'start_date': '2020-01-01 00:00:00',
                'end_date': '2020-01-02 00:00:00',
                'is_draft': False,
                'contact': self.contact,
                'tenant': self.tenant,
            }
        )

        self.assertTrue(form.is_valid())
        pass

    def test_reservation_form_invalid_date(self):
        form = ReservationForm(
            data={
                'name': 'Test Reservation',
                'comments': 'Test Comments',
                'start_date': '2020-01-02 00:00:00',
                'end_date': '2020-01-01 00:00:00',
                'is_draft': False,
                'contact': self.contact,
                'tenant': self.tenant,
            }
        )

        self.assertFalse(form.is_valid())
        pass

    def test_reservation_form_invalid_contact(self):
        form = ReservationForm(
            data={
                'name': 'Test Reservation',
                'comments': 'Test Comments',
                'start_date': '2020-01-01 00:00:00',
                'end_date': '2020-01-02 00:00:00',
                'is_draft': False,
                'contact': 999,
                'tenant': self.tenant,
            }
        )

        self.assertFalse(form.is_valid())
        pass

    def test_reservation_form_invalid_tenant(self):
        form = ReservationForm(
            data={
                'name': 'Test Reservation',
                'comments': 'Test Comments',
                'start_date': '2020-01-01 00:00:00',
                'end_date': '2020-01-02 00:00:00',
                'is_draft': False,
                'contact': self.contact,
                'tenant': 999,
            }
        )

        self.assertFalse(form.is_valid())
        pass

    def test_reservation_form_invalid_is_draft(self):
        form = ReservationForm(
            data={
                'name': 'Test Reservation',
                'comments': 'Test Comments',
                'start_date': '2020-01-01 00:00:00',
                'end_date': '2020-01-02 00:00:00',
                'is_draft': 'invalid',
                'contact': self.contact,
                'tenant': self.tenant,
            }
        )
        logging.debug(form.data.get('is_draft'))

        self.assertFalse(form.is_valid())
        pass


class ClaimFormTestCase(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(
            name='Test Contact'
        )
        self.tenant = Tenant.objects.create(
            name='Test Tenant'
        )
        self.reservation = Reservation.objects.create(
            name='Test Reservation',
            comments='Test Comments',
            start_date='2020-01-01 00:00:00',
            end_date='2020-01-02 00:00:00',
            is_draft=False,
            contact=self.contact,
            tenant=self.tenant,
        )
        self.tag = Tag.objects.create(
            name='Test Tag'
        )

    def test_claim_form(self):
        form = ClaimForm(
            data={
                'restriction': 'EXCLUSIVE',
                'tag': self.tag,
                'reservation': self.reservation,

            }
        )

        self.assertTrue(form.is_valid())
        pass

    def test_claim_form_invalid_reservation(self):
        form = ClaimForm(
            data={
                'restriction': 'EXCLUSIVE',
                'tag': self.tag,
                'reservation': 999,
            }
        )

        self.assertFalse(form.is_valid())
        pass

    def test_claim_form_invalid_tag(self):
        form = ClaimForm(
            data={
                'restriction': 'EXCLUSIVE',
                'tag': 999,
                'reservation': self.reservation,
            }
        )
        self.assertRaises(AttributeError, form.is_valid())
        pass

