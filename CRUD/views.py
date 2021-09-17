from re import I
from rest_framework.views import APIView
from .serializers import MainTableSerializer
from CRUD.models import MainTable as MainTableModel
from datetime import datetime
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import redirect, render
from rest_framework import viewsets


# Create your views here.
def check(check, check_2):
    today = datetime.now()
    print(today)
    now_1 = today.strftime("%Y-%m-%d %H:%M")
    now_2 = today.strftime("%Y-%m-%d %H:%M")
    if check > now_1 or check_2 > now_2:
        return True


class Main(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'index.html'

    def get(self, request, format=None):
        queryset = MainTableModel.objects.all()
        serializer = MainTableSerializer(queryset, many=True)
        serializer_form = MainTableSerializer()
        return Response({'registers': serializer.data,
                         'serializer_form': serializer_form},
                        status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = MainTableSerializer(data=request.data)
        if serializer.is_valid():
            if check(
                    request.data['date_and_time_attention'],
                    request.data['application_date']):
                return Response({'serializer_form': serializer,
                                 'message': "dates cannot be greater than today"},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return redirect('data_table')
        return Response({'serializer_form': serializer},
                        status=status.HTTP_400_BAD_REQUEST)


class MainDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'detail.html'

    def get_object(self, pk):

        try:
            return MainTableModel.objects.get(pk=pk)
        except MainTableModel.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        queryset = self.get_object(pk)
        serializer = MainTableSerializer(queryset)
        return Response({'serializer': serializer,
                         'queryset': queryset},
                        status=status.HTTP_200_OK)

    def post(self, request, pk, format=None):
        queryset = self.get_object(pk)
        serializer = MainTableSerializer(queryset, data=request.data)
        if serializer.is_valid():
            if check(
                    request.data['date_and_time_attention'],
                    request.data['application_date']):
                return Response({'serializer': serializer,
                                 'queryset': queryset,
                                 'message': "dates cannot be greater than today"},
                                status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return redirect('index')
        return Response({'serializer': serializer,
                         'queryset': queryset},
                        status.HTTP_400_BAD_REQUEST)


class MainDelete(APIView):

    def post(self, request, pk, format=None):
        queryset = MainTableModel.objects.get(pk=pk)
        queryset.delete()
        return redirect('index')


def index(request):
    return render(request, 'data_table.html')


class DataTable(viewsets.ModelViewSet):
    queryset = MainTableModel.objects.all()
    serializer_class = MainTableSerializer
