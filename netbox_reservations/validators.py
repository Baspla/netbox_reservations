from django.core.exceptions import ValidationError

from extras.validators import CustomValidator

TIME_FORMAT = '%Y-%m-%d %H:%M'

class ClaimValidator(CustomValidator):
    # Beim Erstellen von Claims wird überprüft ob
    # bei restriction == 'EXCLUSIVE':
    #   ein anderes Claim mit dem selben Tag existiert.
    # bei restriction == 'SHARED':
    #   ein anderes Claim mit dem selben Tag als EXCLUSIVE existiert. Andere mit SHARED sind OK
    def validate(self, instance):
        # if instance.reservation.is_draft:
        #    return
        # Debugging Variablen
        # untersuchtes_objekt = instance.tag.claims
        # dir_von_objekt = dir(untersuchtes_objekt)
        # dict_von_objekt= untersuchtes_objekt.__dict__
        if instance.pk and instance.parent and instance.parent in instance.get_descendants(include_self=True):
            self.fail(
                f"Cannot assign self or child {instance._meta.verbose_name} as parent.",field="parent"
            )
        if instance.pk and instance.parent and instance.parent.reservation != instance.reservation:
            self.fail(
                f"Cannot assign {instance._meta.verbose_name} of other reservation as parent.",field="parent"
            )

        for claim in instance.tag.claims.all():
            # if claim.reservation.is_draft:
            #    continue
            if claim.reservation == instance.reservation:
                continue
            S1 = instance.reservation.start_date
            E1 = instance.reservation.end_date
            S2 = claim.reservation.start_date
            E2 = claim.reservation.end_date
            # Einer der vier Fälle ist redundant
            if (S1 <= S2 <= E1) or (S1 <= E2 <= E1) or (S2 <= S1 <= E2) or (S2 <= E1 <= E2):
                if claim.restriction == 'EXCLUSIVE':
                    self.fail(
                        "Selected tag is already used exclusively by reservation '" + claim.reservation.name + "' from "
                        + S2.strftime(TIME_FORMAT) + " to " + E2.strftime(TIME_FORMAT) + ".",
                        field='tag')
                elif instance.restriction == 'EXCLUSIVE':
                    self.fail(
                        "You can't exclusively claim a tag that is already in shared use by reservation '"
                        + claim.reservation.name + "' from " + S2.strftime(TIME_FORMAT) + " to " + E2.strftime(TIME_FORMAT) + ".",
                        field='restriction')


class ReservationValidator(CustomValidator):

    def validate(self, instance):
        if instance.start_date >= instance.end_date:
            self.fail(
                "Start date must be before end date",
                field='start_date')
        # if instance.is_draft:
        #    return
        if instance.pk is None:  # New instance is being created and has no pk yet. This would cause an error in the next line
            return
        for claim in instance.claims.all():
            try:
                claim.full_clean()
            except ValidationError as e:
                self.fail(
                    "A problem occured when trying to claim tag '" + claim.tag.name + "' with message: " + ''.join(
                        next(iter(e.message_dict.values()))))  # , field='is_draft')
