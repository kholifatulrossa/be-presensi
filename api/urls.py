from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import KelasViewSet, GuruViewSet, SiswaViewSet, KehadiranViewSet, UserViewSet, LoginViewSet

router = DefaultRouter()
router.register(r'kelas', KelasViewSet)
router.register(r'guru', GuruViewSet)
router.register(r'siswa', SiswaViewSet)
router.register(r'kehadiran', KehadiranViewSet)
router.register(r'user', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginViewSet.as_view(), name="login"),
]           

urlpatterns += router.urls
