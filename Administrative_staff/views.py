import random

from django.db.models import Count
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework.response import Response
from .models import *
from Enseignant_candidat.models import *
from Gestion.models import Utilisateur

from django.contrib.auth.decorators import *

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
        candidats = Utilisateur.objects.filter(type='candidat').values(
            "candidat__universite",
            "candidat__specailite",
            "candidat__note_sujet1",
            "candidat__note_sujet2",
            "candidat__moyenne",
            "candidat__id_concours__annee_concours",
            "type",
            "email",
            "nom",
            "prenom",
            "date_naissance",
            "profile_pic"
        )
        enseignants = Utilisateur.objects.filter(type='enseignant').values(
            "enseignant__grade",
            "enseignant__faculte",
            "enseignant__depertement",
            "enseignant__specialite",
            "type",
            "email",
            "nom",
            "prenom",
            "date_naissance",
            "profile_pic"
        )
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
                },
        ).values("enseignant_nom", "enseignant_prenom", "id_sujet__type", "id_sujet__description",
                "id_rapport", "titre", "date", "contenu")
        print(rapport_du_saisi)
        if rapport_du_saisi:
            return Response(rapport_du_saisi)
        else:
            return Response({'rapports' : 'Pas de rapport du saisi'})

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
        nb_total_copie = Candidat.objects.filter(id_concours = concours ,
                                                faculte = fac ,
                                                code_anonyme__isnull = False).count()
        if sujets:
            return Response({"enseignants" : enseignants, "sujets" : sujets,
                            "nb total copie" : nb_total_copie })
        else:
            return Response({'sujets' : 'Les sujets de cette concours pas encore ajouté'})

@api_view(['PUT'])
def setEnseignantsEtSujet(request, id):
    if request.method == 'PUT':
        enseignants = request.data
        concours = Concours.objects.all().order_by('-annee_concours').first().id_concours
        fac = Enseignant.objects.get(id_enseignant=id).faculte
        candidats = Candidat.objects.filter(id_concours = concours ,
                                            faculte = fac ,
                                            code_anonyme__isnull = False).values("code_anonyme")
        for key, value in enseignants.items():
            enseignant = Enseignant.objects.get(id_enseignant = key)
            if value.get("sujet") != None :
                enseignant.id_sujet = Sujet.objects.get(id_sujet = value.get("sujet"))
            else : 
                enseignant.id_sujet = None
            if value.get("nb_copie") != None :
                enseignant.nb_copie = value.get("nb_copie")
            else : 
                enseignant.nb_copie = 0
            enseignant.save()

            candidats_have_corrector = Correction.objects.all().filter(numero_de_correction = value.get("nb_corr"),
                                                                    id_enseignant = key
                                                                    ).values("code_anonyme_candidat")
            candidats_havent_corrector = list(candidats.exclude( code_anonyme__in = candidats_have_corrector
                                                                ).values("code_anonyme"))[0 : value.get("nb_copie")]
            for candidat in candidats_havent_corrector :
                id_candidat = Candidat.objects.get(code_anonyme = candidat.get("code_anonyme"))
                Correction(id_enseignant = enseignant,
                                code_anonyme_candidat = id_candidat,
                                numero_de_correction = value.get("nb_corr")).save()
    return Response({'Etat' : "L'affectation est effectué avec succès"})

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
    return Response({'CodesAnonyme' : 'Les codes anonyme a été généré pour les candidat présent'})

@api_view(['GET'])
def validerNotes(request, id):
    if request.method == 'GET':
        concours = Concours.objects.all().order_by('-annee_concours').first().id_concours
        fac = Enseignant.objects.get(id_enseignant=id).faculte
        candidats = Correction.objects.extra(
                        select={
                            'id_concours': f"select id_concours from candidat where candidat.code_anonyme=code_anonyme_candidat and id_concours = {concours} and faculte = {fac}",
                            'faculte': f"select faculte from candidat where candidat.code_anonyme=code_anonyme_candidat and id_concours = {concours} and faculte = {fac}",
                            },
                        ).values("code_anonyme_candidat").distinct()
        sujets = {}
        for candidat in candidats :
            note1 = Correction.objects.filter(code_anonyme_candidat = candidat.get("code_anonyme_candidat") , numero_de_correction = 1
                                            ).values().first()
            note2 = Correction.objects.filter(code_anonyme_candidat = candidat.get("code_anonyme_candidat") , numero_de_correction = 2
                                            ).values().first()
            if abs(note1.get("note") - note2.get("note")) < 3 :
                n1 = Correction.objects.get(id=note1.get('id'))
                n1.etat = "valide"
                n1.save()
                n2 = Correction.objects.get(id=note2.get('id'))
                n2.etat = "valide"
                n2.save()
                c = Candidat.objects.get(code_anonyme = candidat.get("code_anonyme_candidat"))
                c.note_sujet1 = sum([n1.note,n2.note])/2
                c.save()
            else :
                sujet = Enseignant.objects.get(id_enseignant = note1.get('id_enseignant_id')).id_sujet.id_sujet
                sujet = Sujet.objects.filter(id_sujet = sujet).values().first()
                if sujet.get('id_sujet') not in sujets :
                    enseignants = Enseignant.objects.extra(
                            select={
                                'nom': "select nom from utilisateur where utilisateur.id=id_enseignant",
                                'prenom': "select prenom from utilisateur where utilisateur.id=id_enseignant",
                            },
                        ).filter(faculte = fac , id_sujet = None).values("id_enseignant", "nom", "prenom", "grade", "depertement", "specialite")
                    
                    sujets[ sujet.get('id_sujet')] = {
                                    'description': sujet.get('description'),
                                    'type': sujet.get('type'),
                                    'candidats' : [candidat.get("code_anonyme_candidat")],
                                    'enseignants' : enseignants
                                    }
                else :
                    (sujets.get(sujet.get('id_sujet')))['candidats'].append(candidat.get("code_anonyme_candidat"))
            
            note1 = Correction.objects.all().filter(code_anonyme_candidat = candidat.get("code_anonyme_candidat"),
                                                    numero_de_correction = 1).values()[1]
            note2 = Correction.objects.all().filter(code_anonyme_candidat = candidat.get("code_anonyme_candidat"),
                                                    numero_de_correction = 2).values()[1]
            if abs(note1.get("note") - note2.get("note")) < 3 :
                n1 = Correction.objects.get(id=note1.get('id'))
                n1.etat = "valide"
                n1.save()
                n2 = Correction.objects.get(id=note2.get('id'))
                n2.etat = "valide"
                n2.save()
                c = Candidat.objects.get(code_anonyme = candidat.get("code_anonyme_candidat"))
                c.note_sujet2 = sum([n1.note,n2.note])/2
                c.save()
            else :
                sujet = Enseignant.objects.get(id_enseignant = note1.get('id_enseignant_id')).id_sujet.id_sujet
                sujet = Sujet.objects.filter(id_sujet = sujet).values().first()
                if sujet.get('id_sujet') not in sujets :
                    enseignants = Enseignant.objects.extra(
                            select={
                                'nom': "select nom from utilisateur where utilisateur.id=id_enseignant",
                                'prenom': "select prenom from utilisateur where utilisateur.id=id_enseignant",
                            },
                        ).filter(faculte = fac , 
                        id_sujet = None).values("id_enseignant", "nom", "prenom", "grade", "depertement", "specialite")
                    
                    sujets[ sujet.get('id_sujet')] = {
                                    'description': sujet.get('description'),
                                    'type': sujet.get('type'),
                                    'candidats' : [candidat.get("code_anonyme_candidat")],
                                    'enseignants' : enseignants
                                    }
                else :
                    (sujets.get(sujet.get('id_sujet')))['candidats'].append(candidat.get("code_anonyme_candidat"))
        
        if sujets :
            return Response ({ "CandidatSujet" : sujets})
        else :
            return Response ({ "Etat" : "La validation des notes est effectuée"})

@api_view(['PUT'])
def set3emeEnseignantsEtSujet(request):
    if request.method == 'PUT':
        sujets = request.data
        for key , value in sujets.items() :
            sujet = Sujet.objects.get(id_sujet = key)

            enseignant = Enseignant.objects.get(id_enseignant = value.get('enseignants'))
            enseignant.id_sujet = sujet
            enseignant.nb_copie = len(value.get('candidats'))
            enseignant.save()
            for candidat in value.get('candidats') : 
                candidat_code = Candidat.objects.get(code_anonyme = candidat)
                Correction(id_enseignant = enseignant,
                                code_anonyme_candidat = candidat_code,
                                numero_de_correction = 3).save()
        return Response({'Etat' : "L'affectation est effectué avec succès"})

@api_view(['GET'])
def validerNotesMoyenne(request, id):
    if request.method == 'GET':
        concours = Concours.objects.all().order_by('-annee_concours').first().id_concours
        fac = Enseignant.objects.get(id_enseignant=id).faculte
        candidats = Candidat.objects.filter(id_concours = concours,
                                            faculte = fac,
                                            code_anonyme__isnull = False).values()
        for candidat in candidats : 
            note1 = candidat.get("note_sujet1")
            note2 = candidat.get("note_sujet2")
            if note1 != 0 and note2 != 0 :
                c = Candidat.objects.get(id_candidat = candidat.get('id_candidat_id'))
                c.moyenne = sum([note1, note2])/2
                c.save()
            else :
                id_enseignant = Correction.objects.filter(code_anonyme_candidat = candidat.get("code_anonyme"),
                                                        numero_de_correction = 3).values("id_enseignant")
                sujet = []
                for ens in id_enseignant :
                    sujet.append(Enseignant.objects.filter(id_enseignant = ens.get("id_enseignant")).values("id_sujet"))
                for sujetQ in sujet :
                    for s in sujetQ :
                        enseignants = Enseignant.objects.filter(id_sujet = s.get("id_sujet")).values()
                        notes = []
                        for enseignant in enseignants :
                            note = Correction.objects.filter(code_anonyme_candidat = candidat.get("code_anonyme"),
                                                            id_enseignant = enseignant.get("id_enseignant_id")).values().first()
                            if note :
                                n = Correction.objects.get(id = note.get("id"))
                                n.etat = "valide"
                                n.save()
                                notes.append(note.get("note"))
                        notes.sort(reverse=True)
                        notes = notes[0:2]
                        if note1 == 0 and note2 != 0 :
                            c = Candidat.objects.get(id_candidat = candidat.get('id_candidat_id'))
                            c.note_sujet1 = sum(notes)/2
                            note1 = sum(notes)/2
                            c.moyenne = sum([note1, note2])/2
                            c.save()
                        elif note1 != 0 and note2 == 0 :
                            c = Candidat.objects.get(id_candidat = candidat.get('id_candidat_id'))
                            c.note_sujet2 = sum(notes)/2
                            note2 = sum(notes)/2
                            c.moyenne = sum([note1, note2])/2
                            c.save()
                        else :
                            c = Candidat.objects.get(id_candidat = candidat.get('id_candidat_id'))
                            if c.note_sujet1 == 0 and c.note_sujet2 == 0 :
                                c.note_sujet1 = sum(notes)/2
                                c.save()
                            else :
                                c.note_sujet2 = sum(notes)/2
                                c.moyenne = sum([sum(notes)/2, c.note_sujet1])/2
                                c.save()

        return Response ({ "Etat" : "La validation des notes et le calcul de moyennes est effectuée"})

@api_view(['GET'])
def getDisponibleEmplacementEnseignants(request, id):
    if request.method == 'GET':
        concours = Concours.objects.all().order_by('-annee_concours').first().id_concours
        enseignant = Enseignant.objects.get(id_enseignant = id)
        emplacements = Emplacement.objects.filter(universite = enseignant.universite,
                                                faculte = enseignant.faculte).values("id_emplacement" , "salle","capacite")
        enseignants = Enseignant.objects.extra(
                            select={
                                'nom': "select nom from utilisateur where utilisateur.id=id_enseignant",
                                'prenom': "select prenom from utilisateur where utilisateur.id=id_enseignant",
                            },
                        ).filter(universite = enseignant.universite,
                                faculte = enseignant.faculte).values("id_enseignant", "nom", "prenom", "grade")
        nb_candidats = Candidat.objects.filter(id_concours = concours,
                                            faculte = enseignant.faculte).count()
        emplacement = []
        co = 0
        for empl in emplacements:
            if co < nb_candidats :
                co += empl.get("capacite")
                emplacement.append(empl)
            else :
                break
        return Response ({ "emplacements" : emplacement,
                        "enseignants" : enseignants})

@api_view(['PUT'])
def setEmplacementEnseignantsCandidats(request, id):
    if request.method == 'PUT':
        emplacements = request.data
        concours = Concours.objects.all().order_by('-annee_concours').first().id_concours
        enseignant = Enseignant.objects.get(id_enseignant = id)
        for key , value in emplacements.items() : 
            emplacement = Emplacement.objects.get(id_emplacement = key)
            emplacement.id_enseignant_principal = Enseignant.objects.get(id_enseignant = value.get('id_enseignant_principal'))
            emplacement.id_enseignant_secondaire = Enseignant.objects.get(id_enseignant = value.get('id_enseignant_secondaire'))
            emplacement.save()

            candidats_havent_emplacement = list(Candidat.objects.all(
                                    ).filter(id_emplacement = None,
                                    id_concours = concours,
                                    faculte = enseignant.faculte).values('id_candidat_id'))[0 : emplacement.capacite]
            for candidat in candidats_havent_emplacement : 
                c = Candidat.objects.get(id_candidat = candidat.get('id_candidat_id'))
                c.id_emplacement = emplacement
                c.save()
            
        return Response ({"emplacements" : "L'affectation des enseignants pour la surveillance et les emplacements des candidats été effectée"})

@api_view(['GET'])
def affecterSujetThese (request, id):
    if request.method == 'GET':
        concours = Concours.objects.all().order_by('-annee_concours').first().id_concours
        fac = Enseignant.objects.get(id_enseignant=id).faculte
        candidats = Candidat.objects.filter(id_concours = concours,
                                            faculte = fac,
                                            code_anonyme__isnull = False).order_by('-moyenne').values('id_candidat_id')
        for candidat in candidats :
            choises = Choix.objects.filter(id_candidat = candidat.get('id_candidat_id')).order_by('order').values()
            for choix in choises :
                given = Choix.objects.filter(etat = True , id_these = choix.get('id_these_id'))
                if not given :
                    ch = Choix.objects.get(id = choix.get('id'))
                    ch.etat = True
                    ch.save()
                    break
        theses = Choix.objects.filter(etat = True).values()
        candidats = []
        for these in theses :
            can = Candidat.objects.filter(id_concours = concours, faculte = fac, id_candidat = these.get("id_candidat_id")).extra(
                select={
                    'nom': 'select nom from utilisateur where utilisateur.id=id_candidat',
                    'prenom': 'select prenom from utilisateur where utilisateur.id=id_candidat',
                    'sujet': f'select sujet from these where these.id_these={these.get("id_these_id")}',
                    'description': f'select description from these where these.id_these={these.get("id_these_id")}',
                },
            ).values('nom', 'prenom', 'sujet', 'description', 'universite', 'faculte', 'specailite', 'moyenne')
            if can :
                candidats.append(can)
        return Response ({"candidats" : candidats})

@api_view(['GET'])
def consulterStats (request, id):
    if request.method == 'GET':
        fac = Enseignant.objects.get(id_enseignant=id).faculte

        nb_candidats = Candidat.objects.all().filter(faculte = fac).extra(
                select={
                    'concours': "select annee_concours from concours where candidat.id_concours=concours.id_concours",
                },
            ).values('concours').annotate(nb_candidats=Count("id_concours")).order_by('-concours')
        
        presence_percentage = Candidat.objects.all().filter(faculte = fac).extra(
                select={
                    'concours': "select annee_concours from concours where candidat.id_concours=concours.id_concours",
                    'etat_presence': "select etat_presence from presence where candidat.id_candidat=presence.id_candidat",
                },
            ).values('concours', "etat_presence").annotate(nb_presence=Count('id_concours_id'))
        
        high_moyenne = Candidat.objects.all().filter(faculte = fac).extra(
                select={
                    'concours': "select annee_concours from concours where candidat.id_concours=concours.id_concours",
                },
            ).values('moyenne', 'concours').order_by('-moyenne')
        moyennes = {}
        for hm in high_moyenne :
            if hm.get('concours') not in moyennes :
                moyennes[hm.get('concours')] = hm.get('moyenne')

        nb_reclamation = Reclamation.objects.all().extra(
            select = {
                'concours': "select annee_concours from candidat, concours where candidat.id_candidat=reclamation.id_candidat and candidat.id_concours=concours.id_concours",
            }
        ).values("concours", "id_reclamation")

        reclamations = {}
        for recl in nb_reclamation :
            if recl.get('concours') not in reclamations :
                reclamations[recl.get('concours')] = 1
            else :
                reclamations[recl.get('concours')] += 1

        return Response ({"nbCandidats" : nb_candidats,
                        "presencePercentage" : presence_percentage,
                        "highMoyenne" : moyennes,
                        "nbReclamation" : reclamations
                        })