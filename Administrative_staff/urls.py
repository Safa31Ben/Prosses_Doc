from django.urls import path
from . import views

urlpatterns = [

    path('consulterReclamations/', views.getReclamations, name="consulterReclamations"),
]
