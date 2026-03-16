from django.core.management.base import BaseCommand
from django.db.utils import OperationalError
from django.db import connections
import time


class Command(BaseCommand):
    help = "Database hazır olana kadar bekler"

    def handle(self, *args, **options):
        self.stdout.write("Database bekleniyor...")

        db_conn = None

        while not db_conn:
            try:
                db_conn = connections["default"]
                db_conn.cursor()
            except OperationalError:
                self.stdout.write("Database hazır değil, tekrar deneniyor...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database hazır!"))