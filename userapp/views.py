
import django
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Account, User, Profile
from userapp.serializers import LoginAccountSerializer, UserCreateSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

@api_view(['POST'])
def createUser(request):
    print("Request data:", request)  # Debugging line to check incoming data
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # PUT
# @api_view(['PUT'])
# def updateUser(request, pk):
#     try:
#         user = User.objects.get(pk=pk)
#     except User.DoesNotExist:
#         return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
#     serializer = UserSerializer(user, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # PATCH
# @api_view(['PATCH'])
# def partialUpdateUser(request, pk):
#     try:
#         user = User.objects.get(pk=pk)
#     except User.DoesNotExist:
#         return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

#     serializer = UserSerializer(user, data=request.data, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # DELETE
# @api_view(['DELETE'])
# def deleteUser(request, pk):
#     try:
#         user = User.objects.get(pk=pk)
#         user.delete()
#         return Response({'message': 'User deleted'}, status=status.HTTP_204_NO_CONTENT)
#     except User.DoesNotExist:
#         return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

# get
@api_view(['GET'])
def getUserProfile(request, user_id):

        user = User.objects.get(pk=user_id)
        profile = Profile.objects.get(user=user)
        account = Account.objects.get(user=user)

        data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "username": account.username,
            "age": profile.age,
            "address": profile.address,
        }
        return Response(data)

@api_view(['POST'])
def loginAccount(request):
    print("Login request data:", request.data)  # Debugging line to check incoming data
    serializer = LoginAccountSerializer(data=request.data)  # Debugging line to check serializer state
    if serializer.is_valid():
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

