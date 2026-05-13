from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import OrderTransaction
from .serializers import OrderCreateSerializer, OrderDetailSerializer, OrderListSerializer
from accounts.permissions import IsAdminOrPhysicianOrNurse, IsPhlebotomist, IsLabTechnician


class OrderListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/v1/orders/ — list with filters ?order_status=&patient=
    POST /api/v1/orders/ — place new order
    """
    queryset = OrderTransaction.objects.select_related(
        'patient', 'ordered_by'
    ).prefetch_related('lines').all()
    filterset_fields = ['order_status', 'patient']
    search_fields    = ['order_no', 'patient__mrn', 'patient__patient_name']
    ordering_fields  = ['ordered_at', 'order_status']

    def get_serializer_class(self):
        return OrderCreateSerializer if self.request.method == 'POST' else OrderListSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdminOrPhysicianOrNurse()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        # Inject the ordering user from the JWT token
        serializer.save(ordered_by=self.request.user.profile)


class OrderDetailView(generics.RetrieveAPIView):
    """GET /api/v1/orders/{id}/ — full detail with lines."""
    permission_classes = [IsAuthenticated]
    queryset = OrderTransaction.objects.select_related(
        'patient', 'ordered_by', 'collected_by', 'received_by'
    ).prefetch_related('lines__assay').all()
    serializer_class = OrderDetailSerializer


class OrderCollectView(APIView):
    """
    PATCH /api/v1/orders/{id}/collect/
    Phlebotomist advances order: Ordered → Collected.
    """
    permission_classes = [IsAuthenticated, IsPhlebotomist]

    def patch(self, request, pk):
        try:
            order = OrderTransaction.objects.get(pk=pk)
        except OrderTransaction.DoesNotExist:
            return Response({'detail': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

        if order.order_status != OrderTransaction.STATUS_ORDERED:
            return Response(
                {'detail': 'Only Ordered samples can be collected.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.order_status = OrderTransaction.STATUS_COLLECTED
        order.collected_by = request.user.profile
        order.collected_at = timezone.now()
        order.save()
        return Response({'detail': 'Sample collected.', 'order_no': order.order_no})


class OrderReceiveView(APIView):
    """
    PATCH /api/v1/orders/{id}/receive/
    Lab Technician advances order: Collected → In-Lab.
    """
    permission_classes = [IsAuthenticated, IsLabTechnician]

    def patch(self, request, pk):
        try:
            order = OrderTransaction.objects.get(pk=pk)
        except OrderTransaction.DoesNotExist:
            return Response({'detail': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

        if order.order_status != OrderTransaction.STATUS_COLLECTED:
            return Response(
                {'detail': 'Only Collected orders can be marked In-Lab.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.order_status = OrderTransaction.STATUS_IN_LAB
        order.received_by  = request.user.profile
        order.received_at  = timezone.now()
        order.save()
        return Response({'detail': 'Order marked In-Lab.', 'order_no': order.order_no})