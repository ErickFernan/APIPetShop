from rest_framework.viewsets import ModelViewSet

from saude.models import TreatmentCycle, Service, ExamType, Exam
from saude.serializers import TreatmentCycleSerializer, ServiceSerializer, ExamTypeSerializer, ExamSerializer


class TreatmentCycleViewSet(ModelViewSet):
    queryset = TreatmentCycle.objects.all()
    serializer_class = TreatmentCycleSerializer

class ServiceViewSet(ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ExamTypeViewSet(ModelViewSet):
    queryset = ExamType.objects.all()
    serializer_class = ExamTypeSerializer

class ExamViewSet(ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    