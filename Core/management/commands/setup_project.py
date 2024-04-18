from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            os.system('docker compose -p api_rest_orders -f'
                      f'config{os.sep}docker-compose.yml up -d')
            self.stdout.write("Needed services are up and running")
        except Exception as ex:
            print(f'Error {ex} when try to create dockers')