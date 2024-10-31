from django.contrib import admin
from .models import Kelas, Guru, Siswa, Kehadiran, User

# Register your models here.
@admin.register(Kelas)
class KelasAdmin(admin.ModelAdmin):
    pass

@admin.register(Guru)
class GuruAdmin(admin.ModelAdmin):
    pass

@admin.register(Siswa)
class SiswaAdmin(admin.ModelAdmin):
    pass

@admin.register(Kehadiran)
class KehadiranAdmin(admin.ModelAdmin):
    pass

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
