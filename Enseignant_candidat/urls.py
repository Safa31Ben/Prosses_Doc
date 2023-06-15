from django.urls import path
from . import views

urlpatterns = [
    path(
        "cons_emplacement/<str:pk>",
        views.Consulter_emplacement,
        name="Consulter_emplacement",
    ),
    path("get-notes/<str:pk>", views.NotesList, name="NotesList"),
    path("saisit_notes/<str:pk>", views.saisit_notes, name="saisit_notes"),
    path("faire_rapport/<str:pk>", views.faire_rapport, name="faire_rapport"),
    path("Condidat_list/<str:pk>", views.Condidat_list, name="Condidat_list"),
    path("marquerPresence/<str:pk>", views.marquerPresence, name="marquerPresence"),
    path("prop_these/<str:pk>", views.proposition_theses, name="proposition_theses"),
    path("get-annonece/", views.AnnonceList, name="AnnonceList"),
    path("get-notes-con/<str:pk>", views.NotesList_condidat, name="NotesList_condidat"),
    path("post-these-ordre/<str:pk>", views.these_ordre_post, name="these__ordre_post"),
    path("these_list/", views.these_list, name="these_list"),
    path("faire_reclamation/", views.faire_reclamation, name="faire_reclamation"),
    path(
        "consulter_emplacement_con/<str:pk>",
        views.Consulter_emplacement_con,
        name="Consulter_emplacement_con",
    ),
    path("suivi_correction/<str:pk>", views.suivi_correction, name="suivi_correction"),
]
