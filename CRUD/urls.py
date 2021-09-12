
from django.urls import path
from django.urls.conf import re_path
from . import views 
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.Main.as_view()),
    path('<int:pk>/', views.MainDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)