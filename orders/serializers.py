from rest_framework import serializers
from .models import OrderTransaction, OrderLine
from labtests.models import AssayMaster


class OrderLineSerializer(serializers.ModelSerializer):
    """Shows assay details inside each order line."""
    assay_code  = serializers.CharField(source='assay.assay_code',  read_only=True)
    assay_name  = serializers.CharField(source='assay.assay_name',  read_only=True)
    sample_type = serializers.CharField(source='assay.sample_type', read_only=True)
    unit        = serializers.CharField(source='assay.unit',        read_only=True)
    normal_range = serializers.CharField(source='assay.normal_range', read_only=True)

    class Meta:
        model  = OrderLine
        fields = ['id', 'assay', 'assay_code', 'assay_name', 'sample_type', 'unit', 'normal_range']


class OrderCreateSerializer(serializers.ModelSerializer):
    """Used when Physician/Nurse places a new order. Accepts list of assay IDs."""
    assay_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True
    )

    class Meta:
        model  = OrderTransaction
        fields = ['patient', 'notes', 'assay_ids']

    def validate_assay_ids(self, value):
        if not value:
            raise serializers.ValidationError("At least one assay must be selected.")

        assays = AssayMaster.objects.filter(pk__in=value)

        # Rule 6: only Active assays can be ordered
        inactive = assays.filter(status='Inactive')
        if inactive.exists():
            names = ', '.join(inactive.values_list('assay_name', flat=True))
            raise serializers.ValidationError(
                f"Selected test is inactive and cannot be ordered: {names}"
            )

        # Make sure every ID actually exists
        if assays.count() != len(set(value)):
            raise serializers.ValidationError("One or more assay IDs are invalid.")

        return value

    def _generate_order_no(self):
        """Generates sequential order number: ORD-YYYY0001"""
        from datetime import date
        year   = date.today().year
        prefix = f"ORD-{year}"
        last   = OrderTransaction.objects.filter(
            order_no__startswith=prefix
        ).order_by('-order_no').first()
        seq = 1
        if last:
            try:
                seq = int(last.order_no.replace(prefix, '')) + 1
            except ValueError:
                seq = 1
        return f"{prefix}{seq:04d}"

    def create(self, validated_data):
        assay_ids = validated_data.pop('assay_ids')
        order = OrderTransaction.objects.create(
            order_no     = self._generate_order_no(),
            order_status = OrderTransaction.STATUS_ORDERED,
            **validated_data,
        )
        # Create one OrderLine per selected assay
        for assay_id in assay_ids:
            OrderLine.objects.create(order=order, assay_id=assay_id)
        return order


class OrderListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for worklist views."""
    patient_name     = serializers.CharField(source='patient.patient_name', read_only=True)
    patient_mrn      = serializers.CharField(source='patient.mrn',          read_only=True)
    ordered_by_name  = serializers.CharField(source='ordered_by.full_name', read_only=True)
    order_status_label = serializers.CharField(source='get_order_status_display', read_only=True)
    test_count       = serializers.IntegerField(source='lines.count',        read_only=True)

    class Meta:
        model  = OrderTransaction
        fields = [
            'id', 'order_no', 'patient_name', 'patient_mrn',
            'ordered_by_name', 'ordered_at', 'order_status',
            'order_status_label', 'test_count',
        ]


class OrderDetailSerializer(serializers.ModelSerializer):
    """Full order detail with nested patient, users, and line items."""
    patient_name       = serializers.CharField(source='patient.patient_name', read_only=True)
    patient_mrn        = serializers.CharField(source='patient.mrn',          read_only=True)
    patient_age        = serializers.IntegerField(source='patient.age',        read_only=True)
    patient_gender     = serializers.CharField(source='patient.gender',        read_only=True)
    ordered_by_name    = serializers.CharField(source='ordered_by.full_name',  read_only=True)
    collected_by_name  = serializers.CharField(source='collected_by.full_name', read_only=True, default='')
    received_by_name   = serializers.CharField(source='received_by.full_name',  read_only=True, default='')
    order_status_label = serializers.CharField(source='get_order_status_display', read_only=True)
    lines              = OrderLineSerializer(many=True, read_only=True)

    class Meta:
        model  = OrderTransaction
        fields = '__all__'