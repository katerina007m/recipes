from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from shopapp.models import Order

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Create Order")
        user = User.objects.get(username="admin")
        order = Order.objects.get_or_create(
            delivery_address = "Sadovaya STREET. h.5",
            promocode="SALE123",
            user=user,
        )
        self.stdout.write(f"Created order {order}")