from rest_framework import serializers
from django.contrib.auth import get_user_model
from alumni_app.models import Alumni

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_admin', 'is_member']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            is_admin=validated_data.get('is_admin', False),
            is_member=validated_data.get('is_member', True),
        )
        return user

class AlumniRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alumni
        fields = '__all__'

class UserRegisterWithAlumniSerializer(serializers.ModelSerializer):
    # Alumni fields
    name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    graduation_year = serializers.IntegerField(write_only=True)
    major = serializers.CharField(write_only=True)
    job_position = serializers.CharField(write_only=True)
    company = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(allow_blank=True, required=False, write_only=True)
    linkedin = serializers.URLField(allow_blank=True, required=False, write_only=True)
    status_kerja = serializers.BooleanField(default=False, write_only=True)
    # photo diabaikan untuk SPA (bisa ditambah jika ingin upload file)

    class Meta:
        model = User
        fields = ['username', 'password', 'name', 'email', 'graduation_year', 'major', 'job_position', 'company', 'phone_number', 'linkedin', 'status_kerja']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        alumni_fields = {k: validated_data.pop(k) for k in list(validated_data.keys()) if k not in ['username', 'password']}
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=alumni_fields['email'],
            is_member=True,
            is_admin=False
        )
        Alumni.objects.create(user=user, **alumni_fields)
        return user

    def to_representation(self, instance):
        # Only return username and email after registration
        return {
            'username': instance.username,
            'email': instance.email,
        }
