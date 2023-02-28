from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from extras.models import Tag
from netbox_reservations.models import Reservation, RestrictionChoices, Claim
from tenancy.models import Contact, Tenant

# ./manage.py test netbox_reservations

class ReservationTestCase(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(
            name='Test Contact'
        )
        self.tenant = Tenant.objects.create(
            name='Test Tenant'
        )

        self.reservation_name = 'Test Reservation'
        self.reservation_comments = 'Test Comments'
        self.reservation_start_date = timezone.now()
        self.reservation_end_date = timezone.now() + timedelta(days=1)
        self.reservation_is_draft = False

        self.reservation = Reservation.objects.create(
            name=self.reservation_name,
            comments=self.reservation_comments,
            start_date=self.reservation_start_date,
            end_date=self.reservation_end_date,
            is_draft=self.reservation_is_draft,
            contact=self.contact,
            tenant=self.tenant,
        )

    def test_create_reservation(self):
        self.assertTrue(isinstance(self.reservation, Reservation))
        self.assertEqual(self.reservation.__str__(), self.reservation_name)
        self.assertEqual(self.reservation.name, self.reservation_name)
        self.assertEqual(self.reservation.comments, self.reservation_comments)
        self.assertEqual(self.reservation.start_date, self.reservation_start_date)
        self.assertEqual(self.reservation.end_date, self.reservation_end_date)
        self.assertEqual(self.reservation.is_draft, self.reservation_is_draft)
        self.assertEqual(self.reservation.contact, self.contact)
        self.assertEqual(self.reservation.tenant, self.tenant)

    def test_reservation_status(self):
        self.assertEqual(self.reservation.status(), 'Planned')

        self.reservation.is_draft = True
        self.reservation.save()
        self.assertEqual(self.reservation.status(), 'Draft')

        self.reservation.is_draft = False
        self.reservation.start_date = timezone.now() - timedelta(days=1)
        self.reservation.end_date = timezone.now() + timedelta(days=1)
        self.reservation.save()
        self.assertEqual(self.reservation.status(), 'Active')

        self.reservation.start_date = timezone.now() - timedelta(days=2)
        self.reservation.end_date = timezone.now() - timedelta(days=1)
        self.reservation.save()
        self.assertEqual(self.reservation.status(), 'Overdue')


class ClaimTestCase(TestCase):
    def setUp(self):
        self.reservation = Reservation.objects.create(
            name='Test Reservation',
            comments='Test Comments',
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=1),
            is_draft=False,
            contact=Contact.objects.create(
                name='Test Contact'
            ),
            tenant=Tenant.objects.create(
                name='Test Tenant'
            ),
        )
        self.tag = Tag.objects.create(
            name='Test Tag'
        )

        self.claim_restriction = RestrictionChoices.CHOICES[0][0]
        self.claim_description = 'Test Claim Description'

        self.claim = self.reservation.claims.create(
            reservation=self.reservation,
            restriction=self.claim_restriction,
            tag=self.tag,
            description=self.claim_description,
        )

    def test_create_claim(self):
        self.assertTrue(isinstance(self.claim, Claim))
        self.assertEqual(self.claim.__str__(), "Claim for "+self.tag.name+" by "+self.reservation.name)
        self.assertEqual(self.claim.reservation, self.reservation)
        self.assertEqual(self.claim.restriction, self.claim_restriction)
        self.assertEqual(self.claim.tag, self.tag)
        self.assertEqual(self.claim.description, self.claim_description)
