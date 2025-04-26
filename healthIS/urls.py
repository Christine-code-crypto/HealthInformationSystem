from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, HealthProgramViewSet, signup, login
from rest_framework.authtoken import views as drf_views
from .import views



router = DefaultRouter()
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'healthprograms', HealthProgramViewSet, basename='healthprogram')

urlpatterns = [
    path('api/', include(router.urls)),
    #path('api/clients/search/', ClientSearchView.as_view(), name='client-search'),
    path('api/signup/', signup, name='signup'),
    path('api/login/', login, name='login'),
    path('', views.home, name='home'),
    path('create-program/', views.create_program, name='create_program'),
    path('register-client/', views.register_client, name='register_client'),
    path('clients/', views.client_list, name='client-list'),
    path('clients/<int:client_id>/', views.client_profile, name='client-profile'),
    path('clients/<int:client_id>/enroll/', views.enroll_client, name='enroll_client'),

    

]
