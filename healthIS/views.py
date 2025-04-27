from rest_framework import viewsets, generics,filters
from .models import Client, HealthProgram, Enrollment
from .serializers import ClientSerializer, HealthProgramSerializer, ClientProfileSerializer,EnrollmentSerializer
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate

from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages




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
    '''
class ClientSearchView(generics.ListAPIView):
    serializer_class = ClientSerializer

    def get_queryset(self):
        query = self.request.query_params.get('q', None)
        if query is not None:
            return Client.objects.filter(name__icontains=query)
        return Client.objects.all()
    '''
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
    token = Token.objects.create(user=user)
    return Response({'token': token.key}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):

    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if not user:
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key})

#VIEWS FOR FRONTEND LOGIC

def home(request):
    return render(request, 'healthIS/home.html')

def create_program(request):
    if request.method == 'POST':
        program_name = request.POST.get('program_name')
        description = request.POST.get('description')

        # Save to DB - example assumes HealthProgram model with name & description fields
        program = HealthProgram(name=program_name, description=description)
        program.save()
        
        messages.success(request, f'Program "{program_name}" created successfully!')
        return redirect('home')
    
    return render(request, 'healthIS/create_program.html')

def register_client(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        contact_info = request.POST.get('contact_info')
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        # Save to DB
        client = Client(
            first_name=first_name,
            last_name=last_name,
            email=email,
            contact_info=contact_info,
            dob=dob,
            gender=gender
        )
        client.save()

        messages.success(request, f'Client {first_name} {last_name} registered successfully!')
        return redirect('home')

    return render(request, 'healthIS/register_client.html')




# List clients (with optional search)
def client_list(request):
    query = request.GET.get('q')
    if query:
        clients = Client.objects.filter(
            first_name__icontains=query
        ) | Client.objects.filter(
            last_name__icontains=query
        ) | Client.objects.filter(
            email__icontains=query
        ) | Client.objects.filter(
            contact_info__icontains=query
        )
    else:
        clients = Client.objects.all()

    context = {'clients': clients}
    return render(request, 'healthIS/clients_list.html', context)

# View client profile and enroll in programs
def client_profile(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    enrolled_program_ids = Enrollment.objects.filter(client=client).values_list('program_id', flat=True)
    available_programs = HealthProgram.objects.exclude(id__in=enrolled_program_ids)

    if request.method == 'POST':
        program_id = request.POST.get('program_id')
        program = get_object_or_404(HealthProgram, id=program_id)
        Enrollment.objects.create(client=client, program=program)
        return redirect('client-profile', client_id=client.id)

    enrollments = Enrollment.objects.filter(client=client)

    context = {
        'client': client,
        'available_programs': available_programs,
        'enrollments': enrollments
    }
    return render(request, 'healthIS/client_profile.html', context)

def enroll_client(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    programs = HealthProgram.objects.all()

    if request.method == 'POST':
        program_ids = request.POST.getlist('programs')  
        for pid in program_ids:
            program = HealthProgram.objects.get(id=pid)
            # Prevent duplicate enrollments
            Enrollment.objects.get_or_create(client=client, program=program)
        return redirect('client-profile', client_id=client.id)

    return render(request, 'healthIS/enroll_client.html', {'client': client, 'programs': programs})



def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username or not password1 or not password2:
            messages.error(request, 'Please fill out all fields.')
            return render(request, 'healthIS/signup.html')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'healthIS/signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'healthIS/signup.html')

        user = User.objects.create_user(username=username, password=password1)
        user.save()

        messages.success(request, 'Account created successfully! You can now log in.')
        return redirect('login')

    return render(request, 'healthIS/signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'healthIS/login.html')

    return render(request, 'healthIS/login.html')
