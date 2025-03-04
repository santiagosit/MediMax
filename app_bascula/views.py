import random
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

class BasculaView(APIView):
    def get(self, request):
        peso = round(random.uniform(10, 300), 2)
        return Response({'peso_kg': peso})
