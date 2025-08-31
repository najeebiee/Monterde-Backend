import requests
from django.conf import settings
from apartments.models import Apartment, Unit, Tenant, MeterReading, VisitorLog, Payment

# replace with http://127.0.0.1:8000/api/ if testing locally
API_BASE = "http://127.0.0.1:8000/api/"


def sync_model(model, endpoint):
    """
    Sync all objects of a model to remote API endpoint.
    """
    url = f"{API_BASE}{endpoint}/"
    for obj in model.objects.all():
        data = obj_to_dict(obj)
        try:
            response = requests.post(url, json=data, timeout=10)
            response.raise_for_status()
            print(f"✅ Synced {model.__name__} ID {obj.id}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to sync {model.__name__} ID {obj.id}: {e}")


def obj_to_dict(obj):
    """
    Convert Django model instance into dict for JSON.
    """
    from django.forms.models import model_to_dict
    return model_to_dict(obj)


def run_full_sync():
    sync_model(Apartment, "apartments")
    sync_model(Unit, "units")
    sync_model(Tenant, "tenants")
    sync_model(MeterReading, "meterreadings")
    sync_model(VisitorLog, "visitorlogs")
    sync_model(Payment, "payments")
