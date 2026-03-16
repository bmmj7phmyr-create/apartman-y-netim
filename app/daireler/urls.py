from rest_framework.routers import DefaultRouter
from .views import DaireViewSet, FaturaViewSet, IzsuFaturaTakipViewSet

router = DefaultRouter()
router.register(r'daireler', DaireViewSet)
router.register(r'faturalar', FaturaViewSet)
router.register(r'izsu-faturalar', IzsuFaturaTakipViewSet)

urlpatterns = router.urls