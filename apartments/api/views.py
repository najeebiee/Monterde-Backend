from rest_framework import viewsets
from apartments.models import Apartment, Unit, Tenant, MeterReading, VisitorLog, Payment
from apartments.api.serializers import (
    ApartmentSerializer, UnitSerializer, TenantSerializer,
    MeterReadingSerializer, VisitorLogSerializer, PaymentSerializer
)


class ApartmentViewSet(viewsets.ModelViewSet):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer


class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer


class MeterReadingViewSet(viewsets.ModelViewSet):
    queryset = MeterReading.objects.all()
    serializer_class = MeterReadingSerializer


class VisitorLogViewSet(viewsets.ModelViewSet):
    queryset = VisitorLog.objects.all()
    serializer_class = VisitorLogSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
