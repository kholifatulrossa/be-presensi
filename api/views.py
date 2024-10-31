from django.shortcuts import render, redirect   
from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Kelas, Guru, Siswa, Kehadiran, User
from .serializers import KelasSerializers, GuruSerializers, SiswaSerializers, KehadiranSerializers, UserSerializers, LoginSerializers
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .forms import LoginUser
from django.contrib.auth.hashers import check_password
from rest_framework.authtoken.models import Token
from django.utils.dateparse import parse_date


# Create your views here.
class KelasViewSet(viewsets.ModelViewSet):
    queryset = Kelas.objects.all()
    serializer_class = KelasSerializers
    
class GuruViewSet(viewsets.ModelViewSet):
    queryset = Guru.objects.all()
    serializer_class = GuruSerializers

class SiswaViewSet(viewsets.ModelViewSet):
    queryset = Siswa.objects.all()
    serializer_class = SiswaSerializers
    
    def get_queryset(self):
        queryset = super().get_queryset()
        kelas_id = self.request.query_params.get('kelas_id')
        if kelas_id:
            queryset = queryset.filter(kelas_id=kelas_id)  # Filter berdasarkan kelas_id
        return queryset
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)  # Panggil method 'list' bawaan
        # Tambahkan pesan custom ke dalam response
        return Response({
            'message': 'Data siswa berhasil diambil',
            'output': response.data
        })
    
class KehadiranViewSet(viewsets.ModelViewSet):
    queryset = Kehadiran.objects.all()
    serializer_class = KehadiranSerializers

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter berdasarkan status jika ada
        status = self.request.query_params.get('status')
        if status:
            status_list = status.split(',')  # Pisahkan status yang dipisahkan koma
            queryset = queryset.filter(status__in=status_list)

        # Filter berdasarkan kelas_id jika ada
        kelas_id = self.request.query_params.get('kelas_id')
        if kelas_id:
            queryset = queryset.filter(siswa__kelas_id=kelas_id)

        # Filter berdasarkan siswa_id jika ada
        siswa_id = self.request.query_params.get('siswa_id')
        if siswa_id:
            queryset = queryset.filter(siswa_id=siswa_id)

        # Filter berdasarkan tanggal jika ada
        tanggal = self.request.query_params.get('tanggal')
        if tanggal:
            queryset = queryset.filter(tanggal__startswith=tanggal)
        
        wktdatang = self.request.query_params.get('wktdatang')
        if wktdatang:
            queryset = queryset.filter(wktdatang__startswith=wktdatang)
            
        guru_id = self

        # Urutkan queryset berdasarkan tanggal dan waktu (wktdatang)
        queryset = queryset.order_by('-tanggal', '-wktdatang')

        return queryset


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
        
    def perform_create(self, serializer):
        serializer.save()
        

    def get_queryset(self):
        queryset = super().get_queryset()
        
        siswa_id = self.request.query_params.get('siswa_id')
        if siswa_id:
            queryset = queryset.filter(siswa_id=siswa_id)
            
        guru_id = self.request.query_params.get('guru_id')
        if guru_id:
            queryset = queryset.filter(guru_id=guru_id  )
        
        return queryset


# LOGIN FORM
# class LoginViewSet(viewsets.ViewSet):
#     def login_view(request):
#         identifier = request.data.get('identifier')
#         password = request.data.get('password')

#         # Cek di tabel Guru
#         try:
#             guru = Guru.objects.get(nip=identifier)
#             if check_password(password, guru.password):  # Verifikasi password
#                 return JsonResponse({'message': 'Login berhasil', 'role': 'guru'}, status=200)
#         except Guru.DoesNotExist:
#             pass  # Lanjutkan ke pemeriksaan Siswa

#         # Cek di tabel Siswa
#         try:
#             siswa = Siswa.objects.get(nisn=identifier)
#             if check_password(password, siswa.password):  # Verifikasi password
#                 return JsonResponse({'message': 'Login berhasil', 'role': 'siswa'}, status=200)
#         except Siswa.DoesNotExist:
#             pass  # Identifier tidak ditemukan di kedua tabel

#         return JsonResponse({'error': 'Identitas atau password salah.'}, status=400)    

class LoginViewSet(APIView):
    def post(self, request):
        # Gunakan serializer untuk memvalidasi data input
        serializer = LoginSerializers(data=request.data)
        
        if serializer.is_valid():
            # Jika valid, dapatkan data dari serializer
            validated_data = serializer.validated_data
            
            # Kirim response sukses dengan data user
            return Response({
                'status': validated_data['status'],
                'user_id': validated_data.get('user_id'),
                'guru_id': validated_data.get('guru_id'),
                'siswa_id': validated_data.get('siswa_id'),
            }, status=status.HTTP_200_OK)
        
        # Jika data tidak valid, kembalikan error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)