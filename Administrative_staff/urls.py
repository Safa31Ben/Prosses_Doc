from django.urls import path
from . import views

urlpatterns = [

    path('consulterReclamations/', views.getReclamations, name="consulterReclamations"),
    path('consulterRessourcesHumains/', views.getRessourcesHumains, name="consulterRessourcesHumains"),
    path('partagerAnnonces/', views.partagerAnnonces, name="partagerAnnonces"),
    path('getRapportsDeSaisir/', views.getRapportsDeSaisir, name="getRapportsDeSaisir"),

]
