from django.shortcuts import render

from rest_framework.decorators import api_view
from .serializers import *
from rest_framework.response import Response
from .models import *
from Enseignant_candidat.models import Reclamation

from django.contrib.auth.decorators import *
from rest_framework import status

# Create your views here.

@api_view(['GET'])
def getReclamations(request):
    if request.method == 'GET':
        reclamations = Reclamation.objects.all()
        if reclamations:
            serialiers = ReclamationSerializers(reclamations, many=True)
            return Response(serialiers.data)
        else:
            return Response({'reclamations': 'No reclamations'})