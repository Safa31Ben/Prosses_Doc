from django.urls import path
from . import views

urlpatterns = [

    path('consulterReclamations/', views.getReclamations, name="consulterReclamations"),
    path('repondreReclamations/', views.repondreReclamations, name="repondreReclamations"),
    path('consulterRessourcesHumains/', views.getRessourcesHumains, name="consulterRessourcesHumains"),
    path('partagerAnnonces/', views.partagerAnnonces, name="partagerAnnonces"),
    path('getRapportsDeSaisir/', views.getRapportsDeSaisir, name="getRapportsDeSaisir"),
    path('getEnseignantsEtSujet/<str:id>', views.getEnseignantsEtSujet, name="getEnseignantsEtSujet"),
    path('setEnseignantsEtSujet/<str:id>', views.setEnseignantsEtSujet, name="setEnseignantsEtSujet"),
    path('generCodesAnonyme/', views.generCodesAnonyme, name="generCodesAnonyme"),
    path('validerNotes/<str:id>', views.validerNotes, name="validerNotes"),
    path('set3emeEnseignantsEtSujet/', views.set3emeEnseignantsEtSujet, name="set3emeEnseignantsEtSujet"),
    path('validerNotesMoyenne/<str:id>', views.validerNotesMoyenne, name="validerNotesMoyenne"),
    path('disponibleEmplacementEnseignants/<str:id>', views.getDisponibleEmplacementEnseignants, name="getDisponibleEmplacementEnseignants"),
    path('emplacementEnseignantsCandidats/<str:id>', views.setEmplacementEnseignantsCandidats, name="setEmplacementEnseignantsCandidats"),
    path('affecterSujetThese/<str:id>', views.affecterSujetThese, name="affecterSujetThese"),
    path('consulterStats/<str:id>', views.consulterStats, name="consulterStats"),

]
