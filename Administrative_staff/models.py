from django.db import models


class Concours(models.Model):

    id_concours = models.AutoField(primary_key=True)
    salle = models.CharField(max_length=50, null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    annee_concours = models.DateField(null=False, blank=False)

    class Meta:
        db_table = 'concours'


class Sujet(models.Model):

    id_sujet = models.AutoField(primary_key=True)
    id_concours = models.OneToOneField(Concours, on_delete=models.CASCADE, blank=False,
                                       null=False, db_column='id_concours', to_field='id_concours')

    description = models.CharField(max_length=500, null=False, blank=False)
    type = models.BooleanField(default=False, null=False, blank=False)

    class Meta:
        db_table = 'sujet'


class Annonce(models.Model):

    id_annonce = models.AutoField(primary_key=True)
    contenu = models.CharField(max_length=500, null=False, blank=False)
    date = models.DateTimeField(auto_now=True, null=False, blank=False)

    class Meta:
        db_table = 'annonce'
