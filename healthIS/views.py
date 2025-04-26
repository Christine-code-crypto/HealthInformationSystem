from rest_framework import viewsets,filters
from .models import Client, HealthProgram, Enrollment
from django.shortcuts import render
from .serializers import ClientSerializer, HealthProgramSerializer, ClientProfileSerializer,EnrollmentSerializer
from rest_framework.decorators import action



class HealthProgramViewSet(viewsets.ModelViewSet):
    queryset = HealthProgram.objects.all()
    serializer_class = HealthProgramSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name']

    @action(detail=True, methods=['post'])
    def enroll(self, request, pk=None):
        client = self.get_object()
        program_id = request.data.get('program_id')

        # Check if program_id is provided
        if not program_id:
            return Response({'error': 'Program ID is required.'}, status=400)

        # Check if the program exists
        try:
            program = HealthProgram.objects.get(pk=program_id)
        except HealthProgram.DoesNotExist:
            return Response({'error': 'Health program not found.'}, status=400)

        # Check for duplicate enrollment
        if Enrollment.objects.filter(client=client, program=program).exists():
            return Response({'error': 'Client is already enrolled in this program.'}, status=400)

        # Create the enrollment
        try:
            Enrollment.objects.create(client=client, program=program)
            return Response({'message': f'{client.first_name} {client.last_name} enrolled in {program.name}.'})
        except Exception as e:
            return Response({'error': str(e)}, status=400)    
            
    @action(detail=True, methods=['get'])
    def profile(self, request, pk=None):
        client = self.get_object()
        serializer = ClientProfileSerializer(client)
        return Response(serializer.data)
   
