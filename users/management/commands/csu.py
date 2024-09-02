from django.core.management import BaseCommand

from users.models import Company


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = Company.objects.create(
            email='admin@mail.ru',
            first_name='Admin',
            last_name='Admin',
            is_staff=True,
            is_superuser=True
        )

        user.set_password('2495')
        user.save()