from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from Gestion.models import Utilisateur
from Administrative_staff.models import Concours, Sujet


def validate_decimals(value):
    try:
        if value < 0.0 or value > 20.0:
            raise ValidationError(_(f'(value) must be in the range [0.0, 20.0]'),)
        return round(float(value), 2)
    except:
        raise ValidationError(_(f'(value) is not an integer or a float number'),)

class Candidat(models.Model):
    id_candidat = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, blank=False,
                                       null=False, db_column='id_candidat', to_field='id', primary_key=True)
    universite = models.CharField(max_length=200, blank=False, null=False)
    code_anonyme = models.CharField(db_index=True, max_length=10, unique=True, blank=False, null=True)
    specailite = models.CharField(db_index=True, max_length=25, blank=False, null=False)
    id_concours = models.ForeignKey(Concours, on_delete=models.CASCADE, blank=False,
                                       null=False, db_column='id_concours', to_field='id_concours')
    note_sujet1 = models.FloatField(default=0.00, validators=[validate_decimals], null=False, blank=False)
    note_sujet2 = models.FloatField(default=0.00, validators=[validate_decimals], null=False, blank=False)
    moyenne = models.FloatField(default=0.00, validators=[validate_decimals], null=False, blank=False)

    class Meta:
        db_table = 'candidat'


class Enseignant(models.Model):
    id_enseignant = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, blank=False,
                                         null=False, db_column='id_enseignant', to_field='id', primary_key=True)
    grade = models.CharField(max_length=5, blank=False, null=False)
    faculte = models.CharField(max_length=100, blank=False, null=False)
    depertement = models.CharField(max_length=100, blank=False, null=False)
    specialite = models.CharField(max_length=100, blank=False, null=False)
    id_sujet = models.ForeignKey(Sujet , on_delete=models.CASCADE, blank=False,
                                    null=True, db_column='id_sujet', to_field='id_sujet')
    nb_copie = models.PositiveIntegerField(default = 0, blank=False, null=False)

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
                                                 null=True, db_column='code_anonyme_candidat', to_field='code_anonyme')
    note = models.FloatField(default=0.00, validators=[validate_decimals], null=False, blank=False)
    NB_CORRECTION = [
        (1, '1er'),
        (2, '2éme'),
        (3, '3éme'),
    ]
    numero_de_correction = models.IntegerField(choices=NB_CORRECTION, null=False, blank=False)
    ETAT = [
        ("pas encore corrige", "Pas encore corrigé"),
        ("en cours de correction", "En cours de correction"),
        ("pas valide", "Pas validé"),
        ("valide", "Validé"),
    ]
    etat = models.CharField(max_length=25,choices=ETAT, null=False, blank=False , default="pas encore corrige")

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

class Emplacement(models.Model):
    id_emplacement = models.AutoField(primary_key=True)
    WILAYA = [
        (1,"Adrar"), (2,"Chlef"), (3,"Laghouat"), (4,"Oum El Bouaghi"), (5,"Batna"), (6,"Béjaïa"), (7,"Biskra"), (8,"Bechar"), (9,"Blida"),
        (10,"Bouira"), (11,"Tamanrasset"), (12,"Tbessa"), (13,"Tlemcen"), (14,"Tiaret"), (15,"Tizi Ouzou"), (16,"Alger"), (17,"Djelfa"),
        (18,"Jijel"), (19,"Setif"), (20,"Saida"), (21,"Skikda"), (22,"Sidi Bel Abbes"), (23,"Annaba"), (24,"Guelma"), (25,"Constantine"),
        (26,"Medea"), (27,"Mostaganem"), (28,"M'Sila"), (29,"Mascara"), (30,"Ouargla"), (31,"Oran"), (32,"El Bayadh"), (33,"Illizi"),
        (34,"Bordj Bou Arreridj"), (35,"Boumerdes"), (36,"El Tarf"), (37,"Tindouf"), (38,"Tissemsilt"), (39,"El Oued"), (40,"Khenchela"),
        (41,"Souk Ahras"), (42,"Tipaza"), (43,"Mila"), (44,"Ain Defla"), (45,"Naama"), (46,"Ain Temouchent"), (47,"Ghardaia"), (48,"Relizane"),
        (49,"Timimoun"), (50,"Bordj Baji Mokhtar"), (51,"Ouled Djellal"), (52,"Béni Abbès"), (53,"In Salah"), (54,"In Guezzam"), (55,"Touggourt"),
        (56,"Djanet"), (57,"El M'ghair"), (58,"El Menia"),
    ]
    wilaya = models.IntegerField(choices=WILAYA, null=False, blank=False)
    daira = models.CharField(max_length=100, null=False, blank=False)
    commune = models.CharField(max_length=100, null=False, blank=False)
    universite = models.CharField(max_length=200, null=False, blank=False)
    faculte = models.CharField(max_length=200, null=False, blank=False)
    salle = models.CharField(max_length=100, null=False, blank=False)
    id_enseignant_principal = models.ForeignKey(Enseignant, on_delete=models.CASCADE, blank=False,
                                        null=False, db_column='id_enseignant_principal', to_field='id_enseignant', related_name='enseignant_principal')
    id_enseignant_secondaire = models.ForeignKey(Enseignant, on_delete=models.CASCADE, blank=False,
                                        null=False, db_column='id_enseignant_secondaire', to_field='id_enseignant', related_name='enseignant_secondaire')

    class Meta:
        db_table = 'emplacement'

class Rapport_du_saisi(models.Model):
    id_rapport = models.AutoField(primary_key=True)
    id_enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE, blank=False,
                                         null=False, db_column='id_enseignant', to_field='id_enseignant')
    id_sujet = models.ForeignKey(Sujet, on_delete=models.CASCADE, blank=False,
                                         null=False, db_column='id_sujet', to_field='id_sujet')
    titre = models.CharField(max_length=200, null=False, blank=False)
    date = models.DateTimeField(auto_now=True, null=False, blank=False)
    contenu = models.CharField(max_length=1000, null=False, blank=False)

    class Meta:
        db_table = 'rapportsaisi'