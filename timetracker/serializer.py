from rest_framework import serializers
from .models import Tasks, Projects

class ProjectSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Projects
        fields = ['project_name']