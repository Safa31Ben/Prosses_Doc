from django.contrib.auth.decorators import *
from django.db.models import Q, F

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from .serializers import *
from .models import *


# @permission_classes([IsAuthenticated])
# @allowedUsers(allowedGroups=['enseignant','condidat'])
@api_view(["GET"])
def AnnonceList(request):
    if request.method == "GET":
        Annonces = Annonce.objects.all().order_by("-id_annonce")
        if Annonces:
            serialiers = AnnoncesSerializers(Annonces, many=True)
            return Response(serialiers.data)
        else:
            return Response({"rapport": "Il n'y a pas d'annonce"})


# affichage les notes pour enseignants
@api_view(["GET"])
def NotesList(request, pk):
    if request.method == "GET":
        Notes = Correction.objects.filter(id_enseignant=pk)
        if Notes:
            serialier = NotesSerializers_ens(Notes, many=True)
            return Response(serialier.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


# affichage les notes pour condidats
@api_view(["GET"])
def NotesList_condidat(request, pk):
    if request.method == "GET":
        moyenne = Candidat.objects.get(id_candidat=pk).moyenne
        note_sujet1 = Candidat.objects.get(id_candidat=pk).note_sujet1
        note_sujet2 = Candidat.objects.get(id_candidat=pk).note_sujet2
        if moyenne != 0:
            return Response(
                {
                    "moyenne": moyenne,
                    "note_sujet1": note_sujet1,
                    "note_sujet2": note_sujet2,
                }
            )
        else:
            return Response({"etat": "Les notes ne sont pas encore confirmées"})


# choisir theses classement api
@api_view(["PUT"])
def these_ordre_post(request, pk):
    try:
        candidat = Candidat.objects.get(id_candidat=pk)
    except Candidat.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        data = request.data

        try:
            for item in data:
                id_these = item.get("id_these")
                choix = Choix.objects.get(id_candidat=pk, id_these=id_these)
                if choix:
                    return Response({"choix": "Ce choix a déjà été fait."})
        except Choix.DoesNotExist:
            pass

        for item in data:
            Choix(
                id_these=These.objects.get(id_these=item.get("id_these")),
                id_candidat=candidat,
                order=item.get("order"),
            ).save()

        return Response({"choix": "Vos choix ont été bien soumis."})


# Consulter les condidats
@api_view(["GET"])
def Condidat_list(request, pk):
    if request.method == "GET":
        emplacement = Emplacement.objects.get(id_enseignant_principal=pk).id_emplacement
        candidats = (
            Candidat.objects.extra(
                select={
                    "id": "select id from utilisateur where utilisateur.id=id_candidat",
                    "nom": "select nom from utilisateur where utilisateur.id=id_candidat",
                    "prenom": "select prenom from utilisateur where utilisateur.id=id_candidat",
                    "date_naissance": "select date_naissance from utilisateur where utilisateur.id=id_candidat",
                },
            )
            .filter(id_emplacement=emplacement)
            .values("id", "nom", "prenom", "date_naissance")
        )
        if candidats:
            return Response(candidats)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


# @permission_classes([IsAuthenticated])
# @allowedUsers(allowedGroups=[''])
@api_view(["GET"])
def Consulter_emplacement(request, pk):
    emplacement = Emplacement.objects.filter(
        Q(id_enseignant_principal=pk) | Q(id_enseignant_secondaire=pk)
    ).values("wilaya", "daira", "commune", "universite", "faculte", "salle")
    if emplacement:
        wilaya = [
            (1, "Adrar"),
            (2, "Chlef"),
            (3, "Laghouat"),
            (4, "Oum El Bouaghi"),
            (5, "Batna"),
            (6, "Béjaïa"),
            (7, "Biskra"),
            (8, "Bechar"),
            (9, "Blida"),
            (10, "Bouira"),
            (11, "Tamanrasset"),
            (12, "Tbessa"),
            (13, "Tlemcen"),
            (14, "Tiaret"),
            (15, "Tizi Ouzou"),
            (16, "Alger"),
            (17, "Djelfa"),
            (18, "Jijel"),
            (19, "Setif"),
            (20, "Saida"),
            (21, "Skikda"),
            (22, "Sidi Bel Abbes"),
            (23, "Annaba"),
            (24, "Guelma"),
            (25, "Constantine"),
            (26, "Medea"),
            (27, "Mostaganem"),
            (28, "M'Sila"),
            (29, "Mascara"),
            (30, "Ouargla"),
            (31, "Oran"),
            (32, "El Bayadh"),
            (33, "Illizi"),
            (34, "Bordj Bou Arreridj"),
            (35, "Boumerdes"),
            (36, "El Tarf"),
            (37, "Tindouf"),
            (38, "Tissemsilt"),
            (39, "El Oued"),
            (40, "Khenchela"),
            (41, "Souk Ahras"),
            (42, "Tipaza"),
            (43, "Mila"),
            (44, "Ain Defla"),
            (45, "Naama"),
            (46, "Ain Temouchent"),
            (47, "Ghardaia"),
            (48, "Relizane"),
            (49, "Timimoun"),
            (50, "Bordj Baji Mokhtar"),
            (51, "Ouled Djellal"),
            (52, "Béni Abbès"),
            (53, "In Salah"),
            (54, "In Guezzam"),
            (55, "Touggourt"),
            (56, "Djanet"),
            (57, "El M'ghair"),
            (58, "El Menia"),
        ]
        for item in emplacement:
            item["wilaya"] = next(
                name for code, name in wilaya if code == emplacement[0].get("wilaya")
            )
            principal_emplacement = Emplacement.objects.filter(
                id_enseignant_principal=pk
            ).exists()

        return Response(
            {"emplacement": emplacement, "is_principal": principal_emplacement}
        )
    else:
        return Response({"Etat": "Vous n'est pas affecté pour la surveillance."})


# @permission_classes([IsAuthenticated])
# @allowedUsers(allowedGroups=[''])
@api_view(["GET"])
def Consulter_emplacement_con(request, pk):
    candidat_emplacement = Candidat.objects.get(id_candidat=pk).id_emplacement
    if candidat_emplacement:
        candidat_emplacement = Emplacement.objects.filter(
            id_emplacement=candidat_emplacement.id_emplacement
        ).values("wilaya", "daira", "commune", "universite", "faculte", "salle")
        wilaya = [
            (1, "Adrar"),
            (2, "Chlef"),
            (3, "Laghouat"),
            (4, "Oum El Bouaghi"),
            (5, "Batna"),
            (6, "Béjaïa"),
            (7, "Biskra"),
            (8, "Bechar"),
            (9, "Blida"),
            (10, "Bouira"),
            (11, "Tamanrasset"),
            (12, "Tbessa"),
            (13, "Tlemcen"),
            (14, "Tiaret"),
            (15, "Tizi Ouzou"),
            (16, "Alger"),
            (17, "Djelfa"),
            (18, "Jijel"),
            (19, "Setif"),
            (20, "Saida"),
            (21, "Skikda"),
            (22, "Sidi Bel Abbes"),
            (23, "Annaba"),
            (24, "Guelma"),
            (25, "Constantine"),
            (26, "Medea"),
            (27, "Mostaganem"),
            (28, "M'Sila"),
            (29, "Mascara"),
            (30, "Ouargla"),
            (31, "Oran"),
            (32, "El Bayadh"),
            (33, "Illizi"),
            (34, "Bordj Bou Arreridj"),
            (35, "Boumerdes"),
            (36, "El Tarf"),
            (37, "Tindouf"),
            (38, "Tissemsilt"),
            (39, "El Oued"),
            (40, "Khenchela"),
            (41, "Souk Ahras"),
            (42, "Tipaza"),
            (43, "Mila"),
            (44, "Ain Defla"),
            (45, "Naama"),
            (46, "Ain Temouchent"),
            (47, "Ghardaia"),
            (48, "Relizane"),
            (49, "Timimoun"),
            (50, "Bordj Baji Mokhtar"),
            (51, "Ouled Djellal"),
            (52, "Béni Abbès"),
            (53, "In Salah"),
            (54, "In Guezzam"),
            (55, "Touggourt"),
            (56, "Djanet"),
            (57, "El M'ghair"),
            (58, "El Menia"),
        ]
        for item in candidat_emplacement:
            item["wilaya"] = next(
                name
                for code, name in wilaya
                if code == candidat_emplacement[0].get("wilaya")
            )
        return Response(candidat_emplacement)
    else:
        return Response(
            {
                "candidat_emplacement": "L'emplacement ou vous avez passé le concours n'est pas encore determiné"
            }
        )


# faire rapport au saisit les notes
@api_view(["PUT"])
def faire_rapport(request, pk):
    try:
        enseignants = Enseignant.objects.get(id_enseignant=pk)
    except enseignants.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "PUT":
        data = request.data
        enseignant = Enseignant.objects.get(id_enseignant=pk)
        sujet = enseignant.id_sujet
        Rapport_du_saisi(
            id_enseignant=enseignant,
            id_sujet=sujet,
            titre=data.get("titre"),
            contenu=data.get("contenu"),
        ).save()
        return Response(
            {
                "Etat": f"Votre rapport de saisie de note de correction de sujet <{sujet.description}> est sovgardé avec succée"
            }
        )


@api_view(["POST"])
def saisit_notes(request, pk):
    if request.method == "POST":
        notes = request.data
        for candidat in notes:
            candidat_note = Correction.objects.filter(
                id_enseignant=pk,
                code_anonyme_candidat=candidat.get("code_anonyme_candidat"),
            ).first()
            candidat_note.note = candidat.get("note")
            candidat_note.etat = candidat.get("etat")
            candidat_note.save()
        return Response({"Etat": "Les notes sont saisir avec succés"})


@api_view(["GET"])
def these_list(request):
    if request.method == "GET":
        ids_in_choix = Choix.objects.values_list("id_these", flat=True).filter(
            etat=True
        )
        these_instances = These.objects.exclude(id_these__in=ids_in_choix)

        if these_instances:
            serializer = TheseSerializer(these_instances, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {"theses": "Il n'y a pas encore de nouvelles propositions des thèse"}
            )


@api_view(["PUT"])
def proposition_theses(request, pk):
    try:
        enseignant = Enseignant.objects.get(id_enseignant=pk)
    except Enseignant.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        data = request.data
        data["id_enseignant"] = pk
        serializer = these_Serializers(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["PUT"])
def faire_reclamation(request):
    if request.method == "PUT":
        serializer = Reclamations_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def marquerPresence(request, pk):
    if request.method == "POST":
        presence = request.data
        enseignant = Enseignant.objects.get(id_enseignant=pk)
        for candidat in presence:
            cand = Candidat.objects.get(id_candidat=candidat.get("id_candidat"))
            Presence(
                id_enseignant=enseignant,
                id_candidat=cand,
                etat_presence=candidat.get("etat_presence"),
            ).save()

        return Response({"Etat": "La présence est marqué avec succès"})


@api_view(["GET"])
def suivi_correction(request, pk):
    if request.method == "GET":
        try:
            candidat = Candidat.objects.get(id_candidat=pk)
            presence = Presence.objects.get(id_candidat=pk)
            if presence.etat_presence:
                pas_correction = Correction.objects.filter(
                    code_anonyme_candidat=candidat.code_anonyme,
                    etat="pas encore corrige",
                )
                if len(pas_correction) > 0:
                    return Response(
                        {"pasEncoreCorrige": "Votre copies n'est pas encore corrigée."}
                    )

                correction = Correction.objects.filter(
                    code_anonyme_candidat=candidat.code_anonyme
                )
                pas_valide = (
                    correction.exists()
                    and correction.all().count()
                    == correction.filter(etat="pas valide").count()
                )
                if pas_valide:
                    return Response(
                        {"pasEncoreValide": "Votre notes n'est pas encore validé"}
                    )

                candidats = (
                    Candidat.objects.filter(
                        id_concours=candidat.id_concours,
                        faculte=candidat.faculte,
                        code_anonyme__isnull=False,
                    )
                    .order_by("moyenne")
                    .annotate(
                        nom=F("id_candidat__nom"), prenom=F("id_candidat__prenom")
                    )
                    .values("id_candidat_id", "nom", "prenom")
                )

                candidat_ids = candidats.values_list("id_candidat_id", flat=True)

                has_admitted_candidate = Choix.objects.filter(
                    id_candidat__in=candidat_ids, etat=True
                ).exists()

                if has_admitted_candidate:
                    admis_candidats = []

                    for candidat in candidats:
                        choix_exists = Choix.objects.filter(
                            id_candidat=candidat["id_candidat_id"], etat=True
                        ).exists()

                        if choix_exists:
                            candidat["resultat"] = "Admis(e)"
                        else:
                            candidat["resultat"] = "Ajourné(e)"

                    admis_candidats = list(candidats)

                    return Response({"candidats": admis_candidats.reverse()})
                else:
                    valide = (
                        correction.exists()
                        and correction.all().count()
                        == correction.filter(etat="valide").count()
                    )
                    if valide:
                        moyenne = candidat.moyenne
                        note_sujet1 = candidat.note_sujet1
                        note_sujet2 = candidat.note_sujet2
                        if moyenne != 0:
                            return Response(
                                {
                                    "valide": {
                                        "moyenne": moyenne,
                                        "note_sujet1": note_sujet1,
                                        "note_sujet2": note_sujet2,
                                    }
                                }
                            )
            else:
                return Response({"Etat": "Vous n'avez pas encore passé le concours."})
        except Candidat.DoesNotExist:
            return Response({"Etat": "Vous n'avez pas encore passé le concours."})
        except Presence.DoesNotExist:
            return Response({"Etat": "Vous n'avez pas encore passé le concours."})
