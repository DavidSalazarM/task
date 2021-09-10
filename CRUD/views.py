from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from .serializers import MainTableSerializer
from django.http import JsonResponse

# Create your views here.

class MainTable(APIView):
    def post(self, request, format=None):
        data = JSONParser().parse(request)
        serializer = MainTableSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)