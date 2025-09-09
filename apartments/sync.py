from django.utils import timezone
import requests
import logging
from decimal import Decimal
from datetime import date, datetime
from django.forms.models import model_to_dict
from apartments.models import Apartment, Unit, Tenant, MeterReading, VisitorLog, Payment

logger = logging.getLogger(__name__)

# replace with http://127.0.0.1:8000/api/ if testing locally
API_BASE = "http://127.0.0.1:8000/api/"


def normalize_value(value):
    """
    Normalize values so they're safe for JSON serialization.
    - Decimal -> float
    - date/datetime -> ISO string
    """
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    return value


def obj_to_dict(obj):
    """
    Convert Django model instance into dict for JSON.
    Converts Decimal, date, and datetime automatically.
    """
    data = model_to_dict(obj)

    # Normalize all values
    for key, value in data.items():
        data[key] = normalize_value(value)

    return data


def sync_model(model, endpoint):
    """
    Sync only unsynced objects of a model to remote API endpoint.
    """
    url = f"{API_BASE}{endpoint}/"
    unsynced = model.objects.filter(last_synced__isnull=True)

    for obj in unsynced:
        data = obj_to_dict(obj)
        obj_url = f"{url}{obj.id}/"  # assumes DRF detail endpoint exists

        try:
            # Try update first
            response = requests.put(obj_url, json=data, timeout=10)
            if response.status_code == 404:
                # If not exists remotely, create new
                response = requests.post(url, json=data, timeout=10)

            response.raise_for_status()
            obj.last_synced = timezone.now()
            obj.save(update_fields=["last_synced"])
            print(f"✅ Synced {model.__name__} ID {obj.id}")

        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to sync {model.__name__} ID {obj.id}: {e}")


def run_full_sync():
    """
    Run sync for all major models.
    """
    print("Starting manual sync...")
    sync_model(Apartment, "apartments")
    sync_model(Unit, "units")
    sync_model(Tenant, "tenants")
    sync_model(MeterReading, "meterreadings")
    sync_model(VisitorLog, "visitorlogs")
    sync_model(Payment, "payments")
