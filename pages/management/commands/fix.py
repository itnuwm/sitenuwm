from django.core.management.base import BaseCommand
from pages.models import Webpage


class Command(BaseCommand):
	help = 'Create council page'

	def handle(self, *args, **kwargs):
		pass
