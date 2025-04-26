from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, HealthProgramViewSet
from .import views



router = DefaultRouter()
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'healthprograms', HealthProgramViewSet, basename='healthprogram')

urlpatterns = [
    path('api/', include(router.urls)),
    
    

]
