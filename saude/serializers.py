from rest_framework import serializers

from saude.models import TreatmentCycle, Service, ExamType, Exam


class TreatmentCycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentCycle
        fields = '__all__'

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'

class ExamTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamType
        fields = '__all__'

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'
