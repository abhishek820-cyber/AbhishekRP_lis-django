from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserMaster, UserAccessMaster


class LoginSerializer(serializers.Serializer):
    """Validates credentials and returns user object on success."""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        from django.contrib.auth import authenticate
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            # Generic message — never reveal which field is wrong
            raise serializers.ValidationError("Invalid credentials. Please try again.")
        if not user.is_active:
            raise serializers.ValidationError("This account is disabled.")
        data['user'] = user
        return data


class UserMasterSerializer(serializers.ModelSerializer):
    """Read serializer — returns profile fields plus auth username/email."""
    username = serializers.CharField(source='auth_user.username', read_only=True)
    email    = serializers.EmailField(source='auth_user.email',    read_only=True)

    class Meta:
        model  = UserMaster
        fields = [
            'id', 'username', 'email', 'employee_id', 'full_name',
            'role', 'designation', 'department', 'phone', 'status',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserCreateSerializer(serializers.Serializer):
    """Used by Admin to create a new staff user + linked auth.User in one call."""
    username    = serializers.CharField(max_length=150)
    email       = serializers.EmailField()
    password    = serializers.CharField(write_only=True, min_length=8)
    employee_id = serializers.CharField(max_length=20)
    full_name   = serializers.CharField(max_length=150)
    role        = serializers.ChoiceField(choices=UserMaster.ROLE_CHOICES)
    designation = serializers.CharField(max_length=80)
    department  = serializers.CharField(max_length=80, required=False, allow_blank=True)
    phone       = serializers.CharField(max_length=20, required=False, allow_blank=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already taken.")
        return value

    def validate_employee_id(self, value):
        if UserMaster.objects.filter(employee_id=value).exists():
            raise serializers.ValidationError("Employee ID already exists.")
        return value

    def create(self, validated_data):
        # Step 1: create the Django auth user for login
        auth_user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        # Step 2: create the linked staff profile
        profile = UserMaster.objects.create(
            auth_user   = auth_user,
            employee_id = validated_data['employee_id'],
            full_name   = validated_data['full_name'],
            role        = validated_data['role'],
            designation = validated_data['designation'],
            department  = validated_data.get('department', ''),
            phone       = validated_data.get('phone', ''),
        )
        return profile


class UserAccessSerializer(serializers.ModelSerializer):
    """Serializer for role-based access rules."""
    class Meta:
        model  = UserAccessMaster
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']