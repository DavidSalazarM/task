
from django.urls import path
from django.urls.conf import re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('', views.Main.as_view(), name='index'),
    path('<int:pk>/detail', views.MainDetail.as_view(), name='detail'),
    path('<int:pk>/delete', views.MainDelete.as_view(), name='delete'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
