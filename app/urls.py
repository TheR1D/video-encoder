from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

from app.views import ConverterViewSet


router = routers.DefaultRouter(trailing_slash=False)
router.register("convert", ConverterViewSet, basename="convert")

urlpatterns = []

urlpatterns += router.urls

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += staticfiles_urlpatterns()
