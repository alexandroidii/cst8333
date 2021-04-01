from django.core.management.base import BaseCommand
from users import models.Users


class Command(BaseCommand):

    def handle(self, *args, **options):
        User = get_user_model()
            if not User.objects.filter(username="admin").exists():
                User.objects.create_superuser("admin", "admin@admin.com", "admin")