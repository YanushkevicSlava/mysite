from django.core.management import BaseCommand
from blogapp.models import Tag


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write("Create tag")

        tag = Tag.objects.get_or_create(
            name="Good",
        )
        self.stdout.write(f"Created tag {tag}")