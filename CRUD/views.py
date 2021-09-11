from re import I
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from .serializers import MainTableSerializer
from django.http import JsonResponse
from CRUD.models import MainTable as MainTableModel
from datetime import datetime
from django.http import Http404




# Create your views here.
def check(check):
    today = datetime.now()
    d1 = today.strftime("%Y-%m-%d %H:%M")

    print(check)
    print(d1)
    if check > d1:
        pass
    


  

class MainTable(APIView):

    def get(self, request, format=None):
        queryset = MainTableModel.objects.all()
        serializer = MainTableSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, format=None):
        data = JSONParser().parse(request)
        serializer = MainTableSerializer(data=data)
        check(data['date_and_time_attention'])
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)