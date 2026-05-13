from rest_framework import serializers
from .models import Result


class ResultSerializer(serializers.ModelSerializer):
    """Serializer for entering and reading lab results."""
    assay_code      = serializers.CharField(source='assay.assay_code', read_only=True)
    assay_name      = serializers.CharField(source='assay.assay_name', read_only=True)
    entered_by_name = serializers.CharField(source='entered_by.full_name', read_only=True)

    class Meta:
        model  = Result
        fields = [
            'id', 'order', 'assay', 'assay_code', 'assay_name',
            'result_value', 'unit', 'normal_range', 'flag', 'remarks',
            'entered_by', 'entered_by_name', 'entered_at',
            'verified_by', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'entered_by', 'entered_at', 'created_at', 'updated_at']