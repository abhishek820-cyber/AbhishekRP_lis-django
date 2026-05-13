from rest_framework import serializers
from .models import PatientMaster


class PatientSerializer(serializers.ModelSerializer):

    # Make MRN optional — auto-generated in the view if blank
    mrn = serializers.CharField(max_length=20, required=False, allow_blank=True)

    class Meta:
        model = PatientMaster
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_mrn(self, value):
        if not value:
            return value  # blank is fine — view will generate it
        qs = PatientMaster.objects.filter(mrn=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                "MRN already exists. Please enter a unique Medical Record Number."
            )
        return value

    def validate_patient_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Patient Name is required.")
        return value.strip()

    def validate_age(self, value):
        if value < 0 or value > 150:
            raise serializers.ValidationError(
                "Age must be a whole number between 0 and 150."
            )
        return value

    def validate_gender(self, value):
        if value not in ('Male', 'Female', 'Other'):
            raise serializers.ValidationError("Please select a Gender.")
        return value


class PatientListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list/search — excludes verbose fields."""

    class Meta:
        model = PatientMaster
        fields = ['id', 'mrn', 'patient_name', 'age', 'gender', 'nationality', 'status']