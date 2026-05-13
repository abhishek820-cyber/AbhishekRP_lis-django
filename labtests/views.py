from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import TestMenuMaster, AssayMaster
from .serializers import TestMenuSerializer, AssaySerializer
from accounts.permissions import IsAdmin


class TestMenuListCreateView(generics.ListCreateAPIView):
    queryset         = TestMenuMaster.objects.all()
    serializer_class = TestMenuSerializer
    search_fields    = ['menu_code', 'menu_name', 'department']
    filterset_fields = ['status', 'department']

    def get_permissions(self):
        # Only Admin can create; all authenticated users can read
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]


class TestMenuDetailView(generics.RetrieveUpdateAPIView):
    queryset         = TestMenuMaster.objects.all()
    serializer_class = TestMenuSerializer

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH'):
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]


class AssayListCreateView(generics.ListCreateAPIView):
    queryset         = AssayMaster.objects.select_related('menu').all()
    serializer_class = AssaySerializer
    search_fields    = ['assay_code', 'assay_name']
    filterset_fields = ['status', 'menu']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]


class AssayDetailView(generics.RetrieveUpdateAPIView):
    queryset         = AssayMaster.objects.select_related('menu').all()
    serializer_class = AssaySerializer

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH'):
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]