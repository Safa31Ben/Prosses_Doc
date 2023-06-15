from django.contrib.auth.decorators import *
from django.contrib.auth.models import update_last_login

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

from .serializers import *
from .models import *
from Enseignant_candidat.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ["id", "username", "email", "nom", "prenom", "type"]


class CandidatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidat
        fields = [
            "universite",
            "faculte",
            "specailite"
        ]


class EnseignantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enseignant
        fields = [
            "universite",
            "faculte",
            "specialite",
            "grade",
            "depertement"
        ]


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = [
            "id",
            "type",
            "username",
            "email",
            "nom",
            "prenom",
            "date_naissance"
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    grade = serializers.CharField(required=False)
    type = serializers.CharField(required=False)
    password = serializers.CharField(required=False)

    class Meta:
        model = Utilisateur
        fields = [
            "nom",
            "prenom",
            "date_naissance",
            "password",
            "type",
            "grade",
        ]


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = "__all__"
        read_only_field = ["is_active", "created", "updated"]


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data["full_name"] = Utilisateur.objects.get(
            id=UserSerializer(self.user).data["id"]
        ).get_full_name()
        data["id"] = UserSerializer(self.user).data["id"]
        data["type"] = UserSerializer(self.user).data["type"]
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data


class RegisterSerializer(UserRegisterSerializer):
    password = serializers.CharField(
        max_length=128, min_length=8, write_only=True, required=True
    )
    universite = serializers.CharField(required=False)
    faculte = serializers.CharField(required=False)
    specialite = serializers.CharField(required=False)
    grade = serializers.CharField(required=False)
    depertement = serializers.CharField(required=False)

    class Meta:
        model = Utilisateur
        fields = [
            "type",
            "username",
            "email",
            "nom",
            "prenom",
            "date_naissance",
            "password",
            "universite",
            "faculte",
            "specialite",
            "grade",
            "depertement",
        ]


class EmplacementSerializers(serializers.ModelSerializer):
    class Meta:
        model = Emplacement
        fields = "__all__"


class ConcoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concours
        fields = "__all__"


class SujetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sujet
        fields = ["description", "type"]
