from blog.models import Categorys
from typing import Any
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    help = 'Populate initial categories'

    def handle(self, *args: Any, **options:Any ):

        # Delete existing categories
        Categorys.objects.all().delete()

        categories = ['Sports', 'Technology', 'Science', 'Art', 'Food']

        for cat_data in categories:
            Categorys.objects.create(name=cat_data)

        self.stdout.write(self.style.SUCCESS('Starting category population...'))
