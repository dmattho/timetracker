from functools import wraps
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


from .serializers import UserSerializer

def auth_required(view_func):
    @wraps(view_func)
    @authentication_classes([TokenAuthentication, SessionAuthentication])  
    @permission_classes([IsAuthenticated])
    def _wrapped_view(request, *args, **kwargs):
        return view_func(request, *args, **kwargs)
    return _wrapped_view


@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username = request.data['username'])

    if not user.check_password(request.data['password']):
        return Response({"detail":"Wrong username or password"}, status = status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response({'token': token.key, 'user': serializer.data})

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@auth_required
def test_token(request):
    return Response(f"passed! for {request.user.email}")

@api_view(['POST'])
@auth_required
def logout(request):
    request.user.auth_token.delete()
    return Response({"message": "You have been logged out."}, status = status.HTTP_200_OK)