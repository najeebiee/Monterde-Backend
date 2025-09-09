from django.core.management.base import BaseCommand
from apartments.sync import run_full_sync


class Command(BaseCommand):
    help = "Run a full sync from local SQLite to online MySQL"

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Starting manual sync..."))
        try:
            run_full_sync()
            self.stdout.write(self.style.SUCCESS(
                "✅ Sync completed successfully!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Sync failed: {e}"))
