"""
Django command to wait for databases to be available.
"""

from typing import Any
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    "django command to wait for db"

    def handle(self, *args: Any, **options: Any) :    
        # return super().handle(*args, **options)
        """Entrypoint for command."""
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database available!'))