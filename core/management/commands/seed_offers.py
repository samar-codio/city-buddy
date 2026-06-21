from django.core.management.base import BaseCommand
from core.models import Offer


class Command(BaseCommand):
    help = 'Seed the Offer table with sample products'

    def handle(self, *args, **options):
        # Delete existing offers
        Offer.objects.all().delete()
        self.stdout.write('Cleared existing offers.')

        offers = [
            {
                'title': 'Desi Food Delivery',
                'description': 'Craving biryani, seekh kebabs, or fresh naan? Get authentic desi meals delivered hot to your doorstep — from classic comfort food to your favourite local joints.',
                'image': 'offers/food_delivery.png',
                'is_active': True,
            },
            {
                'title': 'Print & Stationery Hub',
                'description': 'Need assignments printed, reports spiral-bound, or notes laminated? We handle all your academic printing and stationery needs with quick turnaround.',
                'image': 'offers/printing_stationery.png',
                'is_active': True,
            },
            {
                'title': 'Grocery & Essentials',
                'description': 'Fresh fruits, dairy, snacks, and daily household essentials — delivered right to your room. Skip the store run and let CityBuddy handle your grocery list.',
                'image': 'offers/grocery_essentials.png',
                'is_active': True,
            },
            {
                'title': 'Laundry & Dry Cleaning',
                'description': 'Crisp shirts, fresh towels, and professionally cleaned clothes — pick-up and drop-off laundry service so you can focus on what matters most.',
                'image': 'offers/laundry_service.png',
                'is_active': True,
            },
        ]

        for data in offers:
            Offer.objects.create(**data)
            self.stdout.write(self.style.SUCCESS(f'  ✅ Created: {data["title"]}'))

        self.stdout.write(self.style.SUCCESS(f'\nDone! {len(offers)} offers seeded.'))
