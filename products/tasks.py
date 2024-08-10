from celery import shared_task
from .models import Product, Category

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
