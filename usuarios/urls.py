from rest_framework import routers
from django.urls import path, include

from usuarios.views import UserViewSet, UserDocumentViewSet, UserPhotoViewSet, UserAudioViewSet

router = routers.DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(r'document', UserDocumentViewSet, basename='document')
router.register(r'photo', UserPhotoViewSet, basename='photo')
router.register(r'audio', UserAudioViewSet, basename='audio')

urlpatterns = [
    path('', include(router.urls)),
]
