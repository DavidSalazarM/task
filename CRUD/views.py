from re import I
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from .serializers import MainTableSerializer
from django.http import JsonResponse
from CRUD.models import MainTable as MainTableModel
from datetime import datetime
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import BadRequest



# Create your views here.
def check(check, check_2):
    today = datetime.now()
    now_1 = today.strftime("%Y-%m-%d %H:%M")
    now_2 = today.strftime("%Y-%m-%d")
    if check > now_1 or check_2 > now_2:
        raise BadRequest('bad data')
    


  

class MainTable(APIView):

    def get(self, request, format=None):
        queryset = MainTableModel.objects.all()
        serializer = MainTableSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)

    def post(self, request, format=None):
        data = JSONParser().parse(request)
        serializer = MainTableSerializer(data=data)
        check(data['date_and_time_attention'],data['application_date'])
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

class MainTableDetail(APIView):
    def get_object(self, pk):
        try:
            return MainTableModel.objects.get(pk=pk)
        except MainTableModel.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        queryset = self.get_object(pk)
        serializer = MainTableSerializer(queryset)
        return JsonResponse(serializer.data)

    def put(self, request, pk, format=None):
        queryset = self.get_object(pk)
        serializer = MainTableSerializer(queryset, data=request.data)
        check(request.data['date_and_time_attention'],request.data['application_date'])
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    def delete(self, request, pk, format=None):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)