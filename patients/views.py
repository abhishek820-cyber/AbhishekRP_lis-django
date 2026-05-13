from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import PatientMaster
from .serializers import PatientSerializer, PatientListSerializer
from accounts.permissions import IsAdminOrPhysicianOrNurse


def generate_mrn():
    """Auto-generates sequential MRN: PAT-000001, PAT-000002 ..."""
    import re
    last = PatientMaster.objects.filter(
        mrn__startswith='PAT-'
    ).order_by('-id').first()   # order by id, not mrn string
    
    num = 1
    if last:
        try:
            # Extract digits after PAT-
            digits = re.search(r'\d+', last.mrn.split('PAT-')[-1])
            if digits:
                num = int(digits.group()) + 1
        except Exception:
            num = PatientMaster.objects.count() + 1
    return f'PAT-{num:06d}'


class PatientListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/v1/patients/ — search by MRN or name
    POST /api/v1/patients/ — register new patient
    """
    permission_classes = [IsAuthenticated, IsAdminOrPhysicianOrNurse]
    queryset           = PatientMaster.objects.all()
    search_fields      = ['mrn', 'patient_name', 'phone']
    filterset_fields   = ['status', 'gender']

    def get_serializer_class(self):
        return PatientListSerializer if self.request.method == 'GET' else PatientSerializer

    def perform_create(self, serializer):
        # Auto-generate MRN if the user left it blank
        mrn = self.request.data.get('mrn', '').strip()
        if not mrn:
            mrn = generate_mrn()
        serializer.save(mrn=mrn)


class PatientDetailView(generics.RetrieveUpdateAPIView):
    """GET, PUT, PATCH /api/v1/patients/{id}/"""
    permission_classes = [IsAuthenticated, IsAdminOrPhysicianOrNurse]
    queryset           = PatientMaster.objects.all()
    serializer_class   = PatientSerializer