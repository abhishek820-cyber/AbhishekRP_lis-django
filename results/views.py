from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Result
from orders.models import OrderTransaction
from accounts.permissions import IsLabTechnician, IsClinicalStaff


class ResultCreateView(APIView):
    """
    POST /api/v1/orders/{order_id}/results/
    Lab Technician submits results; auto-completes the order.
    Rule 7: order must be In-Lab (status=3) to accept results.
    """
    permission_classes = [IsAuthenticated, IsLabTechnician]

    def post(self, request, order_id):
        order = get_object_or_404(OrderTransaction, pk=order_id)

        # Rule 7 — block result entry unless sample is In-Lab
        if order.order_status not in (
            OrderTransaction.STATUS_IN_LAB,
            OrderTransaction.STATUS_COMPLETED
        ):
            return Response(
                {'detail': 'Results cannot be entered until the sample has reached In-Lab status.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        results_data = request.data.get('results', [])
        if not results_data:
            return Response(
                {'detail': 'No result data provided.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        saved_ids = []
        for item in results_data:
            # Update if result already exists, otherwise create
            result, _ = Result.objects.update_or_create(
                order    = order,
                assay_id = item.get('assay'),
                defaults = {
                    'result_value': item.get('result_value', ''),
                    'unit':         item.get('unit', ''),
                    'normal_range': item.get('normal_range', ''),
                    'flag':         item.get('flag', ''),
                    'remarks':      item.get('remarks', ''),
                    'entered_by':   request.user.profile,
                }
            )
            saved_ids.append(result.id)

        # Advance order to Completed
        order.order_status = OrderTransaction.STATUS_COMPLETED
        order.save()

        return Response(
            {'detail': 'Results saved. Order marked Completed.', 'saved_ids': saved_ids},
            status=status.HTTP_201_CREATED
        )


class OrderReportView(APIView):
    """
    GET /api/v1/orders/{order_id}/report/
    Returns completed lab report as JSON.
    Rule 8: only available when order status = Completed.
    """
    permission_classes = [IsAuthenticated, IsClinicalStaff]

    def get(self, request, order_id):
        order = get_object_or_404(
            OrderTransaction.objects.select_related(
                'patient', 'ordered_by', 'collected_by', 'received_by'
            ).prefetch_related('results__assay', 'lines__assay'),
            pk=order_id
        )

        # Rule 8 — report only for Completed orders
        if order.order_status != OrderTransaction.STATUS_COMPLETED:
            return Response(
                {'detail': 'Report is not available. The order must be Completed before the report can be viewed.'},
                status=status.HTTP_403_FORBIDDEN
            )

        patient = order.patient
        return Response({
            'order_no':     order.order_no,
            'ordered_at':   order.ordered_at,
            'collected_at': order.collected_at,
            'ordered_by':   order.ordered_by.full_name,
            'patient': {
                'mrn':         patient.mrn,
                'name':        patient.patient_name,
                'age':         patient.age,
                'gender':      patient.gender,
                'nationality': patient.nationality,
            },
            'results': [
                {
                    'assay_code':   r.assay.assay_code,
                    'assay_name':   r.assay.assay_name,
                    'result_value': r.result_value,
                    'unit':         r.unit or r.assay.unit,
                    'normal_range': r.normal_range or r.assay.normal_range,
                    'flag':         r.flag,
                    'remarks':      r.remarks,
                }
                for r in order.results.select_related('assay').all()
            ],
        })