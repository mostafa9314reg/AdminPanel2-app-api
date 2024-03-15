"""
Django command to wait for databases to be available.
"""

from typing import Any
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    "django command to wait for db"

    def handle(self, *args: Any, **options: Any) :    
        # return super().handle(*args, **options)
        pass