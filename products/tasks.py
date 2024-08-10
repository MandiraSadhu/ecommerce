from celery import shared_task
from .models import Product, Category
import os

@shared_task
def generate_dummy_products(category_id, num_products):
    category = Category.objects.get(id=category_id)
    for _ in range(num_products):
        Product.objects.create(
            category=category,
            title="Dummy Product",
            description="This is a dummy product.",
            price=10.00,
            status="pending"
        )


@shared_task
def process_video(product_id, video_file_path):
    try:
        # Get the product instance
        product = Product.objects.get(id=product_id)

        # Check file size (20 MB limit)
        file_size = os.path.getsize(video_file_path)
        if file_size > 20 * 1024 * 1024:  # 20 MB
            product.video_status = 'failed'
            product.save()
            return 'File size exceeds 20 MB limit.'

        # Set video status to processing
        product.video_status = 'processing'
        product.save()

        # Process the video (e.g., encoding, compressing)
        # This is where your video processing logic goes
        # Simulating processing with a sleep (replace with actual processing code)
        import time
        for progress in range(0, 101, 10):  # Simulate progress from 0% to 100%
            time.sleep(1)  # Simulating processing delay
            product.video_progress = progress
            product.save()

        # Set video status to completed
        product.video_status = 'completed'
        product.video_progress = 100
        product.save()

        return 'Video processing completed successfully.'

    except Product.DoesNotExist:
        return 'Product not found.'

