from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Client, HealthProgram, Enrollment

class HealthSystemTests(TestCase):
    def setUp(self):
        # Create a test user and obtain a token
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Test data
        self.health_program_data = {'name': 'TB', 'description': 'Tuberculosis Program'}
        self.client_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'dob': '1990-01-01',
            'gender': 'Male',
            'contact_info': '1234567890'
        }

    def test_create_health_program(self):
        """Test creating a health program."""
        response = self.client.post('/api/healthprograms/', self.health_program_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], self.health_program_data['name'])

    def test_register_client(self):
        """Test registering a new client."""
        response = self.client.post('/api/clients/', self.client_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], self.client_data['first_name'])

    def test_enroll_client_in_program(self):
        """Test enrolling a client in one or more programs."""
        # Create a health program
        program = HealthProgram.objects.create(name='Malaria', description='Malaria Program')
        # Register a client
        client_response = self.client.post('/api/clients/', self.client_data)
        self.assertEqual(client_response.status_code, status.HTTP_201_CREATED)  # Ensure client creation succeeded
        client_id = client_response.data['id']
        # Enroll the client in the program
        enroll_response = self.client.post(f'/api/clients/{client_id}/enroll/', {'program_id': program.id})
        self.assertEqual(enroll_response.status_code, status.HTTP_200_OK)
        self.assertIn('enrolled in', enroll_response.data['message'])

    def test_search_client(self):
        """Test searching for a client."""
        # Register a client
        client_response = self.client.post('/api/clients/', self.client_data)
        self.assertEqual(client_response.status_code, status.HTTP_201_CREATED)  # Ensure client creation succeeded
        # Search for the client
        search_response = self.client.get('/api/clients/', {'search': 'John'})
        self.assertEqual(search_response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(search_response.data), 0)
        self.assertEqual(search_response.data[0]['first_name'], 'John')

    def test_view_client_profile(self):
        """Test viewing a client's profile."""
        # Register a client
        client_response = self.client.post('/api/clients/', self.client_data)
        self.assertEqual(client_response.status_code, status.HTTP_201_CREATED)  # Ensure client creation succeeded
        client_id = client_response.data['id']
        # View the client's profile
        profile_response = self.client.get(f'/api/clients/{client_id}/profile/')
        self.assertEqual(profile_response.status_code, status.HTTP_200_OK)
        self.assertEqual(profile_response.data['first_name'], 'John')
        self.assertIn('enrolled_programs', profile_response.data)

    def test_expose_client_profile_via_api(self):
        """Test exposing the client profile via an API."""
        # Register a client
        client_response = self.client.post('/api/clients/', self.client_data)
        self.assertEqual(client_response.status_code, status.HTTP_201_CREATED)  # Ensure client creation succeeded
        client_id = client_response.data['id']
        # View the client's profile via API
        api_response = self.client.get(f'/api/clients/{client_id}/profile/')
        self.assertEqual(api_response.status_code, status.HTTP_200_OK)
        self.assertEqual(api_response.data['first_name'], 'John')
        self.assertIn('enrolled_programs', api_response.data)
