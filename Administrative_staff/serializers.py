from dataclasses import fields
from rest_framework import serializers
from .models import *
from Enseignant_candidat.models import Reclamation

class ReclamationSerializers(serializers.ModelSerializer):

    class Meta:
        model = Reclamation
        fields = '__all__'
