from django.core.management import BaseCommand
from blogapp.models import Author


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write("Create author")

        author = Author.objects.get_or_create(
            name="James Bond",
            bio="Author from England"
        )
        self.stdout.write(f"Created author {author}")
