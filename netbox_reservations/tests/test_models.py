from datetime import timedelta

from django.core.exceptions import ValidationError
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
        self.reservation_description = 'Test Comments'
        self.reservation_start_date = timezone.now() + timedelta(days=1)
        self.reservation_end_date = timezone.now() + timedelta(days=2)
        self.reservation_is_draft = False

        self.reservation = Reservation.objects.create(
            name=self.reservation_name,
            description=self.reservation_description,
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
        self.assertEqual(self.reservation.description, self.reservation_description)
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
            description='Test Comments',
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
        self.assertEqual(self.claim.__str__(), "Claim for " + self.tag.name + " by " + self.reservation.name)
        self.assertEqual(self.claim.reservation, self.reservation)
        self.assertEqual(self.claim.restriction, self.claim_restriction)
        self.assertEqual(self.claim.tag, self.tag)
        self.assertEqual(self.claim.description, self.claim_description)


class CollisionTestCase(TestCase):
    def setUp(self):
        self.reservationA = Reservation.objects.create(
            name='Test Reservation A',
            description='Test Comments',
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=2),
            is_draft=False,
            contact=Contact.objects.create(
                name='Test Contact A'
            ),
            tenant=Tenant.objects.create(
                slug='test-tenant-a',
                name='Test Tenant A'
            ),
        )
        self.reservationB = Reservation.objects.create(
            name='Test Reservation B',
            description='Test Comments',
            start_date=timezone.now() + timedelta(days=1),
            end_date=timezone.now() + timedelta(days=3),
            is_draft=True,
            contact=Contact.objects.create(
                name='Test Contact B'
            ),
            tenant=Tenant.objects.create(
                slug='test-tenant-b',
                name='Test Tenant B'
            ),
        )
        self.reservationC = Reservation.objects.create(
            name='Test Reservation C',
            description='Test Comments',
            start_date=timezone.now() - timedelta(days=4),
            end_date=timezone.now() + timedelta(days=4),
            is_draft=False,
            contact=Contact.objects.create(
                name='Test Contact C'
            ),
            tenant=Tenant.objects.create(
                slug='test-tenant-c',
                name='Test Tenant C'
            ),
        )

        self.tag = Tag.objects.create(
            slug='test-tag',
            name='Test Tag'
        )
        pass

    def test_collision_A_B(self):
        self.claimA = self.reservationA.claims.create(
            reservation=self.reservationA,
            restriction=RestrictionChoices.CHOICES[0][0],
            tag=self.tag,
            description='Test Claim Description',
        )
        self.assertRaises(ValidationError, self.reservationB.claims.create,
            reservation=self.reservationB,
            restriction=RestrictionChoices.CHOICES[0][0],
            tag=self.tag,
            description='Test Claim Description',
        )
        pass

    def test_collision_A_C(self):
        self.claimA = self.reservationA.claims.create(
            reservation=self.reservationA,
            restriction=RestrictionChoices.CHOICES[0][0],
            tag=self.tag,
            description='Test Claim Description',
        )
        self.assertRaises(ValidationError, self.reservationC.claims.create,
            reservation=self.reservationC,
            restriction=RestrictionChoices.CHOICES[1][0],
            tag=self.tag,
            description='Test Claim Description',
        )
        pass

    def test_collision_B_C(self):
        self.claimB = self.reservationB.claims.create(
            reservation=self.reservationB,
            restriction=RestrictionChoices.CHOICES[1][0],
            tag=self.tag,
            description='Test Claim Description',
        )
        self.claimC = self.reservationC.claims.create(
            reservation=self.reservationC,
            restriction=RestrictionChoices.CHOICES[1][0],
            tag=self.tag,
            description='Test Claim Description',
        )
        pass
