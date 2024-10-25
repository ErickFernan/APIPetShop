from utils.views import BaseViewSet
from utils.roles import PRODUCTS_ROLES

from saude.models import TreatmentCycle, Service, ExamType, Exam
from saude.serializers import TreatmentCycleSerializer, ServiceSerializer, ExamTypeSerializer, ExamSerializer


class TreatmentCycleViewSet(BaseViewSet):
    queryset = TreatmentCycle.objects.all()
    serializer_class = TreatmentCycleSerializer
    roles_required = PRODUCTS_ROLES

class ServiceViewSet(BaseViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    roles_required = PRODUCTS_ROLES

class ExamTypeViewSet(BaseViewSet):
    queryset = ExamType.objects.all()
    serializer_class = ExamTypeSerializer
    roles_required = PRODUCTS_ROLES

class ExamViewSet(BaseViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    roles_required = PRODUCTS_ROLES

    folder_prefix = 'exams'
    