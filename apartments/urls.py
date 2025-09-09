# apartments/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apartments.api.views import (
    ApartmentViewSet, UnitViewSet, TenantViewSet,
    MeterReadingViewSet, VisitorLogViewSet, PaymentViewSet
)

router = DefaultRouter()
router.register(r"apartments", ApartmentViewSet)
router.register(r"units", UnitViewSet)
router.register(r"tenants", TenantViewSet)
router.register(r"meterreadings", MeterReadingViewSet)
router.register(r"visitorlogs", VisitorLogViewSet)
router.register(r"payments", PaymentViewSet)

urlpatterns = router.urls
