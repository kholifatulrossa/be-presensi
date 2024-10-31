from django.shortcuts import render

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model


User = get_user_model

# Create your views here.
class CustomTokenObtainPairSerializers(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.nama
        if user.guruId:
            token['guru_nama'] = user.guruId.nama
        if user.siswaId:
            token['siswa_nama'] = user.siswaId.nama
            
        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializers
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = serializer.validated_data['access']

        # Menyimpan token ke dalam model pengguna
        user.jwt_token = token
        user.save()

        return Response({
            'refresh': serializer.validated_data['refresh'],
            'access': token,
        }, status=status.HTTP_200_OK)
        