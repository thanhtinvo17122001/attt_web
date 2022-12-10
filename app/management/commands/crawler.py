from django.core.management.base import BaseCommand
from app.modules.crawler import crawler_service

class Command(BaseCommand):
  def handle(self, *args, **options):
    crawler_service.run()
