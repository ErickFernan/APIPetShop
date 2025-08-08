from rest_framework import routers
from django.urls import path, include

from saude.views import TreatmentCycleViewSet, ServiceViewSet, ExamTypeViewSet, ExamViewSet

router = routers.DefaultRouter()
router.register(r'treatment_cicle', TreatmentCycleViewSet, basename='treatment_cicle')
router.register(r'service', ServiceViewSet, basename='service')
router.register(r'exam_type', ExamTypeViewSet, basename='exam_type')
router.register(r'exam', ExamViewSet, basename='exam')

urlpatterns = [
    path('', include(router.urls)),
]
