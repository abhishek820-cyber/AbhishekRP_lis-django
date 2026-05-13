from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
import rest_framework.authentication

from .models import UserMaster, UserAccessMaster
from .serializers import (
    LoginSerializer, UserMasterSerializer,
    UserCreateSerializer, UserAccessSerializer
)
from .permissions import IsAdmin


class LoginView(APIView):
    """
    POST /api/v1/auth/login/
    Returns JWT access + refresh tokens and the user's role.
    No authentication required for this endpoint.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Generate JWT token pair
        refresh = RefreshToken.for_user(user)

        # Get role safely — superusers may not have a profile yet
        try:
            role      = user.profile.role
            full_name = user.profile.full_name
        except UserMaster.DoesNotExist:
            role      = 'Admin'
            full_name = user.username

        return Response({
            'access':    str(refresh.access_token),
            'refresh':   str(refresh),
            'role':      role,
            'full_name': full_name,
            'user_id':   user.id,
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    POST /api/v1/auth/logout/
    Blacklists the refresh token so it cannot be reused.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = RefreshToken(request.data['refresh'])
            token.blacklist()
            return Response({'detail': 'Logged out successfully.'})
        except (KeyError, TokenError):
            return Response(
                {'detail': 'Invalid or missing refresh token.'},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserListCreateView(generics.ListCreateAPIView):
    """GET /api/v1/users/ and POST /api/v1/users/ — Admin only."""
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset           = UserMaster.objects.select_related('auth_user').all()
    search_fields      = ['full_name', 'employee_id', 'role']

    def get_serializer_class(self):
        # Use creation serializer for POST, read serializer for GET
        return UserCreateSerializer if self.request.method == 'POST' else UserMasterSerializer


class UserDetailView(generics.RetrieveUpdateAPIView):
    """GET /api/v1/users/{id}/ and PUT — Admin only."""
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset           = UserMaster.objects.select_related('auth_user').all()
    serializer_class   = UserMasterSerializer


class UserAccessListCreateView(generics.ListCreateAPIView):
    """GET/POST /api/v1/users/access/ — Admin only."""
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset           = UserAccessMaster.objects.all()
    serializer_class   = UserAccessSerializer
    filterset_fields   = ['role_name', 'module_name']

class SessionTokenView(APIView):
    """
    GET /api/v1/auth/session-token/
    Issues a JWT token to an already session-authenticated user.
    This lets template pages (logged in via Django session) call
    the JWT-protected REST API without a separate login step.
    """
    # Allow session-authenticated users (no JWT needed here)
    authentication_classes = [
        rest_framework.authentication.SessionAuthentication
    ]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        refresh = RefreshToken.for_user(request.user)
        return Response({
            'access':  str(refresh.access_token),
            'refresh': str(refresh),
        })