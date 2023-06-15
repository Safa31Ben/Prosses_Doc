from rest_framework import serializers
from .models import *
from Administrative_staff.models import Annonce


class AnnoncesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Annonce
        fields = "__all__"


class emplacementSerializers(serializers.ModelSerializer):
    class Meta:
        model = Emplacement
        fields = ["wilaya", "daira", "commune", "universite", "faculte", "salle"]


class NotesSerializers_ens(serializers.ModelSerializer):
    class Meta:
        model = Correction
        fields = [
            "note",
            "numero_de_correction",
            "code_anonyme_candidat",
        ]


class NotesSerializers_condidat(serializers.ModelSerializer):
    class Meta:
        model = Correction
        fields = ["note", "numero_de_correction"]


class these_Serializers(serializers.ModelSerializer):
    class Meta:
        model = These
        fields = "__all__"


class these_ordre_Serializers(serializers.ModelSerializer):
    class Meta:
        model = Choix
        fields = "__all__"


class Condidat_Serializers(serializers.ModelSerializer):
    class Meta:
        model = Candidat
        fields = "__all__"


class Raport_serializers(serializers.ModelSerializer):
    class Meta:
        model = Rapport_du_saisi
        fields = "__all__"


class note_serializer(serializers.ModelSerializer):
    class Meta:
        model = Correction
        fields = "__all__"


class Reclamations_serializer(serializers.ModelSerializer):
    class Meta:
        model = Reclamation
        fields = "__all__"


class Correctionclassement_serializer(serializers.ModelSerializer):
    class Meta:
        model = Correction
        fields = ["etat"]


class CorrectionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Correction
        fields = ["note", "numero_de_correction", "etat", "code_anonyme_candidat"]


class noteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Correction
        fields = "__all__"


class TheseSerializer(serializers.ModelSerializer):
    class Meta:
        model = These
        fields = ["id_these", "sujet", "description"]
