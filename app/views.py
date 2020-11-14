from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from app.models import MediaFile
from app.serializers import ConverterSerializer


class ConverterViewSet(RetrieveModelMixin, CreateModelMixin, GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = ConverterSerializer
    queryset = MediaFile.objects.all()
