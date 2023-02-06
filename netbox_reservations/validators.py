from django.core.exceptions import ValidationError

from extras.validators import CustomValidator


class ClaimValidator(CustomValidator):

    # Beim Erstellen von Claims wird überprüft ob
    # bei restriction == 'EXCLUSIVE':
    #   ein anderes Claim mit dem selben Tag existiert.
    # bei restriction == 'SHARED':
    #   ein anderes Claim mit dem selben Tag als EXCLUSIVE existiert. Andere mit SHARED sind OK
    def validate(self, instance):
        if instance.reservation.is_draft:
            return
        # Debugging Variablen
        # untersuchtes_objekt = instance.tag.claims
        # dir_von_objekt = dir(untersuchtes_objekt)
        # dict_von_objekt= untersuchtes_objekt.__dict__
        for claim in instance.tag.claims.all():
            if claim.reservation.is_draft:
                continue
            S1 = instance.reservation.start_date
            E1 = instance.reservation.end_date
            S2 = claim.reservation.start_date
            E2 = claim.reservation.end_date
            # Einer der vier Fälle ist redundant
            if (S1 <= S2 <= E1) or (S1 <= E2 <= E1) or (S2 <= S1 <= E2) or (S2 <= E1 <= E2):
                if claim.restriction == 'EXCLUSIVE':
                    self.fail(
                        "Selected tag is already used exclusively by reservation '" + claim.reservation.name + "'",
                        field='tag')
                elif instance.restriction == 'EXCLUSIVE':
                    self.fail(
                        "You can't exclusively claim a tag that is already in shared use by reservation '" + claim.reservation.name + "'",
                        field='tag')


class ReservationValidator(CustomValidator):

    def validate(self, instance):
        if instance.is_draft:
            return
        for claim in instance.claims.all():
            try:
                claim.full_clean()
            except ValidationError as e:
                self.fail(
                    "A problem occured when trying to claim tag '" + claim.tag.name + "' with message: " + ''.join(
                        e.message_dict['tag']), field='is_draft')
