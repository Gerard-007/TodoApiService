from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import response, status, permissions
from rest_framework.generics import GenericAPIView
from authentication.serializers import LoginSerializer, RegisterSerialiser


class AuthUserAPIView(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    #serializer_class=

    def get(self, request):
        user = request.user
        serializer = RegisterSerialiser(user)
        return response.Response({'user': serializer.data})


class RegisterAPIView(GenericAPIView):
    authentication_classes = []
    serializer_class = RegisterSerialiser

    def post(self, request):
        user_serializer = self.serializer_class(data=request.data)

        if user_serializer.is_valid():
            user_serializer.save()
            return response.Response(user_serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(GenericAPIView):

    authentication_classes = []
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get("email", None)
        password = request.data.get("password", None)

        user = authenticate(username=email, password=password)

        if user:
            user_serializer = self.serializer_class(user)
            return response.Response(user_serializer.data, status=status.HTTP_200_OK)
        return response.Response({"message": "Invalid credentials, try again"}, status=status.HTTP_401_UNAUTHORIZED)
