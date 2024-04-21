from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            os.system(f'docker compose -p api_rest_orders --env-file .{os.sep}config{os.sep}.env up --build -d')
            self.stdout.write("Needed services are up and running")
        except Exception as ex:
            print(f'Error {ex} when try to create dockers')