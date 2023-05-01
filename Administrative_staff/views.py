import random

from django.shortcuts import render

from rest_framework.decorators import api_view
from .serializers import *
from rest_framework.response import Response
from .models import *
from Enseignant_candidat.models import *
from Gestion.models import Utilisateur

from django.contrib.auth.decorators import *
from rest_framework import status

@api_view(['GET'])
def getReclamations(request):
    if request.method == 'GET':
        reclamations = Reclamation.objects.all()
        if reclamations:
            serialiers = ReclamationSerializers(reclamations, many=True)
            return Response(serialiers.data)
        else:
            return Response({'reclamations' : 'No reclamations'})
        
@api_view(['GET'])
def getRessourcesHumains(request):
    if request.method == 'GET':
        candidats = Utilisateur.objects.extra(
            select={
                'universite': "select universite from candidat where utilisateur.id=id_candidat",
                'specailite': "select specailite from candidat where utilisateur.id=id_candidat",
                'note_sujet1': "select note_sujet1 from candidat where utilisateur.id=id_candidat",
                'note_sujet2': "select note_sujet2 from candidat where utilisateur.id=id_candidat",
                'moyenne': "select moyenne from candidat where utilisateur.id=id_candidat",
                'concours': "select annee_concours from candidat, concours where candidat.id_concours=concours.id_concours",
                },
        ).filter(type = 'candidat'
        ).values("universite", "specailite", "note_sujet1", "note_sujet2", "moyenne", "concours",
                "type", "email", "nom", "prenom", "date_naissance", "profile_pic")
        enseignants = Utilisateur.objects.extra(
            select={
                'grade': "select grade from enseignant where utilisateur.id=id_enseignant",
                'faculte': "select faculte from enseignant where utilisateur.id=id_enseignant",
                'depertement': "select depertement from enseignant where utilisateur.id=id_enseignant",
                'specialite': "select specialite from enseignant where utilisateur.id=id_enseignant",
                },
        ).filter(type = 'enseignant'
        ).values("grade", "faculte", "depertement" , "specialite",
                "type", "email", "nom", "prenom", "date_naissance", "profile_pic")
        
        if candidats and enseignants:
            return Response({"enseignants" : enseignants, "candidats" : candidats})
        elif candidats:
            return Response({"candidats" : candidats})
        elif enseignants:
            return Response({"enseignants" : enseignants})
        else:
            return Response({'RessourcesHumains' : 'No enseignants, No candidats'})

@api_view(['POST'])
def partagerAnnonces(request):
    if request.method == 'POST':
        serializer = AnnonceSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
@api_view(['GET'])
def getRapportsDeSaisir(request):
    if request.method == 'GET':
        rapport_du_saisi = Rapport_du_saisi.objects.extra(
            select = {
                'enseignant_nom': "select nom from utilisateur where utilisateur.id=id_enseignant",
                'enseignant_prenom': "select prenom from utilisateur where utilisateur.id=id_enseignant",
                'sujet_type': "select type from sujet where sujet.id_sujet=id_sujet",
                'sujet_description': "select description from sujet where sujet.id_sujet=id_sujet",
                },
        ).values("enseignant_nom", "enseignant_prenom", "sujet_type", "sujet_description",
                "id_rapport", "titre", "date", "contenu")
        if rapport_du_saisi:
            return Response(rapport_du_saisi)
        else:
            return Response({'rapports' : 'pas de rapport du saisi'})
        
@api_view(['GET'])
def getEnseignantsEtSujet(request, id):
    if request.method == 'GET':
        concours = Concours.objects.all().order_by('-annee_concours').first().id_concours
        sujets = Sujet.objects.filter(id_concours=concours).values("id_sujet", "description", "type")
        fac = Enseignant.objects.get(id_enseignant=id).faculte
        enseignants = Enseignant.objects.extra(
            select={
                'nom': "select nom from utilisateur where utilisateur.id=id_enseignant",
                'prenom': "select prenom from utilisateur where utilisateur.id=id_enseignant",
            },
        ).filter(faculte = fac
        ).values("id_enseignant", "nom", "prenom", "grade", "depertement", "specialite")

        if sujets:
            return Response({"enseignants" : enseignants, "sujets" : sujets })
        else:
            return Response({'sujets' : 'Les sujets de cette concours pas encore ajouté'})

@api_view(['PUT'])
def setEnseignantsEtSujet(request):
    if request.method == 'PUT':
        enseignant_sujet = request.data
        enseignant_update_list = []

        for key, value in enseignant_sujet.items():
            enseignant = Enseignant.objects.get(id_enseignant = key)
            if value != None :
                enseignant.id_sujet = Sujet.objects.get(id_sujet = value)
            else : 
                enseignant.id_sujet = None
            enseignant_update_list.append(enseignant)
        
        Enseignant.objects.bulk_update(enseignant_update_list, ['id_sujet'])

    return Response({'state' : 'Les sujet de concours sont affecté'})

@api_view(['GET'])
def generCodesAnonyme(request):
    if request.method == 'GET':
        concours = Concours.objects.all().order_by('-annee_concours').first().id_concours
        candidats = Candidat.objects.all().filter(id_concours = concours).values("id_candidat")
        for candidat in candidats :
            candidat = candidat.get("id_candidat")
            presence = Presence.objects.get(id_candidat = candidat).etat_presence
            if presence :
                not_unique = True
                while not_unique:
                    unique_ref = random.randint(1000000000, 9999999999)
                    if not Candidat.objects.filter(code_anonyme = unique_ref):
                        not_unique = False
                c = Candidat.objects.get(id_candidat = candidat)
                if c.code_anonyme == None :
                    c.code_anonyme = unique_ref
                    c.save()
    return Response({'Codes Anonyme' : 'Les codes anonyme a été généré pour les candidat présent'})