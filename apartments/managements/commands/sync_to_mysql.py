from django.core.management.base import BaseCommand
from django.db import connections, transaction
from apartments.models import Apartment, Unit, Tenant


class Command(BaseCommand):
    help = "Sync tenants from SQLite to MySQL"

    def handle(self, *args, **kwargs):
        sqlite = connections['default']
        mysql = connections['online']

        # Fetch tenants from SQLite
        tenants = Tenant.objects.using('default').all()
        units = Unit.objects.using('default').all()
        apartments = Apartment.objects.using('default').all()
        self.stdout.write(f"Found {tenants.count()} tenants from SQLite")

        with transaction.atomic(using='online'):
            for tenant in tenants:
                # Check if tenant already exists in MySQL
                if not Tenant.objects.using('online').filter(id=tenant.id).exists():
                    # Create new tenant in MySQL
                    Tenant.objects.using('online').create(
                        id=tenant.id,
                        name=tenant.name,
                        email=tenant.email,
                        phone=tenant.phone,
                        apartment=tenant.apartment
                    )
                    self.stdout.write(f"Synced tenant {tenant.name} to MySQL")
                else:
                    self.stdout.write(
                        f"Tenant {tenant.name} already exists in MySQL, skipping.")
