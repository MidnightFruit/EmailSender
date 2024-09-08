from django.core.management import BaseCommand

from sender.tasks import send_messages

class Command(BaseCommand):
    """Комманда для отправки рассылки"""

    def handle(self, *args, **options):
        send_messages()