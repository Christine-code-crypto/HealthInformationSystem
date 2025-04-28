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

'''
class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'
'''

class EnrollmentSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(
        queryset=Client.objects.all(),
        slug_field='email'  # or use first_name + last_name combined differently
    )
    program = serializers.SlugRelatedField(
        queryset=HealthProgram.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = Enrollment
        fields = '__all__'

class MultiEnrollmentSerializer(serializers.Serializer):
    client = serializers.SlugRelatedField(queryset=Client.objects.all(), slug_field='email')
    programs = serializers.ListField(
        child=serializers.CharField(),
        write_only=True
    )

    def validate_programs(self, value):
        # Check all programs exist
        programs = HealthProgram.objects.filter(name__in=value)
        if len(programs) != len(set(value)):
            raise serializers.ValidationError("One or more programs do not exist.")
        return value

    def create(self, validated_data):
        client = validated_data['client']
        program_names = validated_data['programs']
        enrollments = []

        for name in program_names:
            program = HealthProgram.objects.get(name=name)
            enrollment, created = Enrollment.objects.get_or_create(client=client, program=program)
            enrollments.append(enrollment)

        return enrollments

class ClientProfileSerializer(serializers.ModelSerializer):
    enrolled_programs = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name','dob', 'contact_info', 'date_registered', 'enrolled_programs']

    def get_enrolled_programs(self, obj):
        enrollments = Enrollment.objects.filter(client=obj)
        return [enrollment.program.name for enrollment in enrollments]
