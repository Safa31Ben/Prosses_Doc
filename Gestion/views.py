from django.contrib.auth.decorators import *
from Enseignant_candidat.models import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from .serializers import *
from .models import *


class LoginViewSet(ModelViewSet, TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class RegistrationViewSet(ModelViewSet, TokenObtainPairView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                user = Utilisateur.objects.get(
                    username=serializer.validated_data["username"]
                )
            except ObjectDoesNotExist:
                user = Utilisateur.objects.create_user(
                    type=serializer.validated_data["type"],
                    username=serializer.validated_data["username"],
                    password=serializer.validated_data["password"],
                    email=serializer.validated_data["email"],
                    nom=serializer.validated_data["nom"],
                    prenom=serializer.validated_data["prenom"],
                    date_naissance=serializer.validated_data["date_naissance"],
                )

                if user.type == "candidat":
                    candidat = Candidat(
                        id_candidat=user,
                        id_concours=Concours.objects.all()
                        .order_by("-annee_concours")
                        .first(),
                        universite=serializer.validated_data.get("universite"),
                        faculte=serializer.validated_data.get("faculte"),
                        specailite=serializer.validated_data.get("specialite"),
                    )
                    candidat.save()
                elif user.type in ["enseignant", "président-du-CFD", "vice-doyen"]:
                    enseignant = Enseignant(
                        id_enseignant=user,
                        grade=serializer.validated_data.get("grade"),
                        universite=serializer.validated_data.get("universite"),
                        faculte=serializer.validated_data.get("faculte"),
                        depertement=serializer.validated_data.get("depertement"),
                        specialite=serializer.validated_data.get("specialite"),
                    )
                    enseignant.save()

            refresh = RefreshToken.for_user(user)
            res = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
            return Response(
                {
                    "user": serializer.data["username"],
                    "refresh": res["refresh"],
                    "token": res["access"],
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors)


class UtilisateurUpdateViewSet(ModelViewSet):
    serializer_class = UserUpdateSerializer
    http_method_names = [
        "put",
        "patch",
    ]

    def get_queryset(self):
        pk = self.kwargs["pk"]
        return Utilisateur.objects.filter(id=pk)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        if "password" in serializer.validated_data:
            password = serializer.validated_data["password"]
            hashed_password = make_password(password)
            serializer.validated_data["password"] = hashed_password

        self.perform_update(serializer)
        if "grade" in serializer.validated_data:
            enseignant = Enseignant.objects.get(id_enseignant=self.kwargs["pk"])
            enseignant.grade = serializer.validated_data["grade"]
            enseignant.save()

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


@api_view(["GET"])
def user_list(request):
    if request.method == "GET":
        Utilisateurs = Utilisateur.objects.filter(is_active=True)
        if Utilisateurs:
            serialier = UserSerializer(Utilisateurs, many=True)
            return Response(serialier.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def user_detail(request, pk):
    if request.method == "GET":
        user_detail = Utilisateur.objects.filter(id=pk).first()

        if user_detail:
            if user_detail.type == "candidat":
                serializer = CandidatSerializer(user_detail.candidat)
                user_serializer = UserDetailSerializer(user_detail)
                data = {
                    "user_detail": user_serializer.data,
                    "candidat_detail": serializer.data,
                }
                return Response(data)
            elif user_detail.type in ["enseignant", "président-du-CFD", "vice-doyen"]:
                serializer = EnseignantSerializer(user_detail.enseignant)
                user_serializer = UserDetailSerializer(user_detail)
                data = {
                    "user_detail": user_serializer.data,
                    "enseignant_detail": serializer.data,
                }
                return Response(data)
            else:
                serializer = UserDetailSerializer(user_detail)

            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


# make the account inactive
@api_view(["DELETE"])
def DeleteUser(request, pk):
    if request.method == "DELETE":
        serializer = Utilisateur.objects.get(id=pk)
        serializer.is_active = False
        serializer.save()
        return Response(status=status.HTTP_202_ACCEPTED)


@api_view(["POST"])
def AddEmplacement(request):
    if request.method == "POST":
        serializer = EmplacementSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            errors = serializer.errors
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def AddConcoursAndSujet(request):
    if request.method == "POST":
        concours_serializer = ConcoursSerializer(data=request.data)

        if concours_serializer.is_valid():
            concours = concours_serializer.save()
            sujet_serializer = SujetSerializer(
                data=request.data.get("sujets", []), many=True
            )
            if sujet_serializer.is_valid():
                sujet_serializer.save(id_concours=concours)
            else:
                return Response(
                    sujet_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
            return Response(concours_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                concours_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
