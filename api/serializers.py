from rest_framework import serializers
from .models import Guru, Kehadiran, Siswa, Kelas, User
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import check_password
from django.db import transaction


class KelasSerializers(serializers.ModelSerializer):
    class Meta:
        model = Kelas
        fields = '__all__'
        
class GuruSerializers(serializers.ModelSerializer):
    kelas_id = serializers.PrimaryKeyRelatedField(queryset=Kelas.objects.all())
    kelas = KelasSerializers(read_only=True)
    
    class Meta:
        model = Guru
        fields = ['id','nip', 'nama', 'kelas_id', 'kelas']
        
class SiswaSerializers(serializers.ModelSerializer):
    kelas_id = serializers.PrimaryKeyRelatedField(queryset=Kelas.objects.all())
    kelas = KelasSerializers(read_only=True)

    class Meta:
        model = Siswa
        fields = ['id','nisn', 'nama', 'kelas_id', 'kelas']

        
class KehadiranSerializers(serializers.ModelSerializer):
    siswa_id = serializers.PrimaryKeyRelatedField(queryset=Siswa.objects.all())  # Pastikan ini hanya menerima ID
    siswa = SiswaSerializers(read_only=True)  # Read-only untuk mencegah input langsung dari objek siswa

    class Meta:
        model = Kehadiran
        fields = ['id', 'tanggal', 'wktdatang', 'wktpulang', 'status', 'siswa_id', 'keterangan', 'siswa']


class UserSerializers(serializers.ModelSerializer):
    guru_id = serializers.PrimaryKeyRelatedField(queryset=Guru.objects.all(), required=False)
    siswa_id = serializers.PrimaryKeyRelatedField(queryset=Siswa.objects.all(), required=False)

    class Meta: 
        model = User
        fields = ['id','password', 'guru_id', 'siswa_id']

    def validate(self, attrs):
        # Ensure at least one of guru or siswa is provided
        if not attrs.get('guru_id') and not attrs.get('siswa_id'):
            raise serializers.ValidationError("Either 'guru' or 'siswa' must be provided.")
        return attrs
    
    def create(self, validated_data):
        # Hash the password before saving
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Hash the password if it's being updated
        password = validated_data.get('password', None)
        if password:
            validated_data['password'] = make_password(password)
        
        return super().update(instance, validated_data)

class LoginSerializers(serializers.Serializer):
    identifier = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, data):
        identifier = data.get('identifier')
        password = data.get('password')

        try:
            # Start database transaction
            with transaction.atomic():
                user = None

                # Determine which table to search based on identifier length
                if len(identifier) <= 10:
                    # Search in Siswa table by NISN
                    siswa = Siswa.objects.get(nisn=identifier)
                    user = User.objects.get(siswa=siswa)
                elif len(identifier) > 15:
                    # Search in Guru table by NIP
                    guru = Guru.objects.get(nip=identifier)
                    user = User.objects.get(guru=guru)

                # Validate password
                if user and check_password(password, user.password):
                    # If successful, return user info (ID, token, etc.)
                    return {
                        'status': 'success',
                        'user_id': user.id,
                        'guru_id': user.guru_id if user.guru_id else None,
                        'siswa_id': user.siswa_id if user.siswa_id else None,
                    }
                else:
                    raise serializers.ValidationError('Incorrect password or user not found.')

        except ObjectDoesNotExist:
            raise serializers.ValidationError('User with this identifier was not found.')

        return data
