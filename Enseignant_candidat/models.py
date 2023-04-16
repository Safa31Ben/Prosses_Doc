from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from Gestion.models import Utilisateur
from Administrative_staff.models import Concours


def validate_decimals(value):
    try:
        if value < 0.0 or value > 20.0:
            raise ValidationError(_(f'{value} must be in the range [0.0, 20.0]'),)
        return round(float(value), 2)
    except:
        raise ValidationError(_(f'{value} is not an integer or a float number'),)
        
class Candidat(models.Model):
    id_candidat = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, blank=False,
                                       null=False, db_column='id_candidat', to_field='id', primary_key=True)
    universite = models.CharField(max_length=200, blank=False, null=False)
    code_anonyme = models.CharField(db_index=True, max_length=25, unique=True, blank=False, null=True)
    specailite = models.CharField(db_index=True, max_length=25, blank=False, null=False)

    id_concours = models.ForeignKey(Concours, on_delete=models.CASCADE, blank=False,
                                       null=False, db_column='id_concours', to_field='id_concours')
    moyenne = models.FloatField(default=0.00, validators=[validate_decimals], null=False, blank=False)
    class Meta:
        db_table = 'candidat'


class Enseignant(models.Model):
    id_enseignant = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, blank=False,
                                         null=False, db_column='id_enseignant', to_field='id', primary_key=True)
    grade = models.CharField(max_length=5, blank=False, null=False)

    class Meta:
        db_table = 'enseignant'

class Notification_Candidats(models.Model):

    id_notification_candidat = models.AutoField(primary_key=True)
    id_candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE, blank=False,
                                       null=False, db_column='id_candidat', to_field='id_candidat')
    contenu = models.CharField(max_length=500, blank=False, null=False)
    date_notification = models.DateTimeField(auto_now=True, null=False, blank=False)
    vu = models.BooleanField(default=False, null=False, blank=False)

    class Meta:
        db_table = 'notification_candidats'


class Notification_Enseignants(models.Model):

    id_notification_enseignant = models.AutoField(primary_key=True)
    id_enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE, blank=False,
                                         null=False, db_column='id_enseignant', to_field='id_enseignant')
    contenu = models.CharField(max_length=500, null=False, blank=False)
    date_notification = models.DateTimeField(auto_now=True, null=False, blank=False)
    vu = models.BooleanField(default=False, null=False, blank=False)

    class Meta:
        db_table = 'notification_enseignants'

class Correction(models.Model):

    id_enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE, blank=False,
                                         null=False, db_column='id_enseignant', to_field='id_enseignant')
    code_anonyme_candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE, blank=False,
                                                 null=False, db_column='code_anonyme_candidat', to_field='code_anonyme')
    note = models.FloatField(default=0.00, validators=[validate_decimals], null=False, blank=False)
    NB_CORRECTION = [
        (1, '1er'),
        (2, '2éme'),
        (3, '3éme'),
    ]
    numero_de_correction = models.IntegerField(choices=NB_CORRECTION, null=False, blank=False)

    class Meta:
        unique_together = (('id_enseignant', 'code_anonyme_candidat'),)
        db_table = 'correction'

class Presence(models.Model):

    id_enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE, blank=False,
                                         null=False, db_column='id_enseignant', to_field='id_enseignant')
    id_candidat = models.OneToOneField(Candidat, on_delete=models.CASCADE, blank=False,
                                       null=False, db_column='id_candidat', to_field='id_candidat')
    etat_presence = models.BooleanField(default=False, null=False, blank=False)
    date = models.DateTimeField(auto_now=True, null=False, blank=False)

    class Meta:
        unique_together = (('id_enseignant', 'id_candidat'),)
        db_table = 'presence'

class Reclamation(models.Model):

    id_reclamation = models.AutoField(primary_key=True)
    id_candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE, blank=False,
                                       null=False, db_column='id_candidat', to_field='id_candidat')
    contenu = models.CharField(max_length=500, null=False, blank=False)
    date = models.DateTimeField(auto_now=True, null=False, blank=False)
    Reponse = models.CharField(max_length=500, null=True, blank=False)

    class Meta:
        db_table = 'reclamation'

class These(models.Model):

    id_these = models.AutoField(primary_key=True)
    id_enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE, blank=False,
                                         null=False, db_column='id_enseignant', to_field='id_enseignant')
    sujet = models.CharField(max_length=200, null=False, blank=False)
    description = models.CharField(max_length=500, null=False, blank=False)

    class Meta:
        db_table = 'these'

class Choix(models.Model):

    id_candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE, blank=False,
                                       null=False, db_column='id_candidat', to_field='id_candidat')
    id_these = models.ForeignKey(These, on_delete=models.CASCADE, blank=False,
                                    null=False, db_column='id_these', to_field='id_these')

    etat = models.BooleanField(default=False, null=False, blank=False)
    order = models.PositiveIntegerField(null=False, blank=False)

    class Meta:
        unique_together = (('id_these', 'id_candidat'),)
        db_table = 'choix' 