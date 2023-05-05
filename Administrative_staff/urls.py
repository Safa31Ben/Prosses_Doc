from django.urls import path
from . import views

urlpatterns = [

    path('consulterReclamations/', views.getReclamations, name="consulterReclamations"),
    path('consulterRessourcesHumains/', views.getRessourcesHumains, name="consulterRessourcesHumains"),
    path('partagerAnnonces/', views.partagerAnnonces, name="partagerAnnonces"),
    path('getRapportsDeSaisir/', views.getRapportsDeSaisir, name="getRapportsDeSaisir"),
    path('getEnseignantsEtSujet/<str:id>', views.getEnseignantsEtSujet, name="getEnseignantsEtSujet"),
    path('setEnseignantsEtSujet/<str:id>', views.setEnseignantsEtSujet, name="setEnseignantsEtSujet"),
    path('generCodesAnonyme/', views.generCodesAnonyme, name="generCodesAnonyme"),
    path('validerNotes/<str:id>', views.validerNotes, name="validerNotes"),
    path('validerNotesMoyenne/<str:id>', views.validerNotesMoyenne, name="validerNotesMoyenne"),

]
