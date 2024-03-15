from django.urls import re_path
from . import views

urlpatterns = [
    re_path('create_project', views.create_project)
   
]