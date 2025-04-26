from rest_framework import serializers
from .models import Client, HealthProgram, Enrollment

class HealthProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthProgram
        fields = ['id', 'name', 'description', 'date_created']

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'

class ClientProfileSerializer(serializers.ModelSerializer):
    enrolled_programs = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name','dob', 'contact_info', 'date_registered', 'enrolled_programs']

    def get_enrolled_programs(self, obj):
        enrollments = Enrollment.objects.filter(client=obj)
        return [enrollment.program.name for enrollment in enrollments]