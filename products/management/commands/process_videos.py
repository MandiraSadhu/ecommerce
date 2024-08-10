from django.core.management.base import BaseCommand
from products.models import Product
from products.tasks import process_video

class Command(BaseCommand):
    help = 'Process videos for all products'

    def handle(self, *args, **kwargs):
        products = Product.objects.filter(video__isnull=False, video_status='pending')
        for product in products:
            process_video.delay(product_id=product.id, video_file_path=product.video.path)
            self.stdout.write(self.style.SUCCESS(f'Started processing for product {product.id}'))