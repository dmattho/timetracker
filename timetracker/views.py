from rest_framework.decorators import api_view
from .serializer import Projects
from rest_framework.response import Response

@api_view(['POST'])
def create_project(request):
    return Response({})
