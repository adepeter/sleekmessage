import os
import pathlib

from cryptography.fernet import Fernet

from django.conf import settings
from django.core.management import BaseCommand

SETTINGS_DIR = settings.SETTINGS_DIR

class Command(BaseCommand):
    def handle(self, *args, **options):
        # file = pathlib.Path('secrets.key')
        file = os.path.join(SETTINGS_DIR, 'secrets.key')
        with open(file, 'ab') as f:
            print(f.readlines())