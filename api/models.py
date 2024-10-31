from django.db import models
from enum import Enum
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from secrets import token_hex


# Create your models here.
class Kelas(models.Model):
    nama = models.CharField(max_length=20)
    
    class Meta: 
        db_table = 'kelas'
    
    def __int__(self):
        return self.id
    
class Guru(models.Model):
    nama = models.CharField(max_length=200)
    nip = models.CharField(max_length=25, unique=True)
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'guru'
        
    def __int__(self):
        return self.id

    
class Siswa(models.Model):
    nama = models.CharField(max_length=200)
    nisn = models.CharField(max_length=10, unique=True)
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'siswa'
        
    def __int__(self):
        return self.id

    
class Status(Enum):
    HADIR = 'HADIR'
    IZIN = 'IZIN'
    SAKIT = 'SAKIT'
    TELAT = 'TELAT'
    PULANG = 'PULANG'
    
    
class Kehadiran(models.Model):
    tanggal = models.CharField(max_length=50 )
    wktdatang = models.CharField(max_length=10, null=True)
    wktpulang = models.CharField(max_length=10, null=True, blank=True)
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=10,
        choices=[(tag.value, tag.name) for tag in Status],
    )
    keterangan = models.TextField(max_length=1000, null=True, blank=True)
    
    def clean(self):
        # Pastikan keterangan wajib diisi jika status adalah 'IZIN' atau 'SAKIT'
        if self.status in [Status.IZIN.value, Status.SAKIT.value] and not self.keterangan:
            raise ValidationError({
                'keterangan': 'Keterangan wajib diisi jika status adalah IZIN atau SAKIT.'
            })
        # Reset keterangan jika status selain 'IZIN' atau 'SAKIT'
        if self.status not in [Status.IZIN.value, Status.SAKIT.value]:
            self.keterangan = None

    class Meta:
        db_table = 'kehadiran'
        
    def save(self, *args, **kwargs):
        self.clean()  # Panggil clean() sebelum save
        super().save(*args, **kwargs)
    
    
    def __str__(self):
        return self.status

class User(models.Model):
    password = models.CharField(max_length=250)
    token = models.CharField(max_length=255, null=True)
    guru = models.ForeignKey(Guru, on_delete=models.CASCADE, null=True, blank=True, related_name='user')
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE, null=True, blank=True, related_name='user')

    class Meta:
        db_table = 'user'
    def __str__(self):
        return f'User (ID: {self.id}, Siswa: {self.siswa.nisn if self.siswa else "None"}, Guru: {self.guru.nip if self.guru else "None"})'


    def generate_token(self):
        self.token = token_hex(16)  # generate token when needed
        self.save()


