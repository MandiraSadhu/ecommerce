from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .permissions import IsAdminOrStaff, IsAdmin
from .utils import encrypt_data, decrypt_data
from django.shortcuts import get_object_or_404
from .tasks import process_video
import csv
from django.http import HttpResponse
from rest_framework import pagination

# Category Views
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrStaff]

    def create(self, request, *args, **kwargs):
        request.data['name'] = decrypt_data(request.data['name'])
        return super().create(request, *args, **kwargs)

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrStaff]

    def update(self, request, *args, **kwargs):
        request.data['name'] = decrypt_data(request.data['name'])
        return super().update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.delete()

# Product Views
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrStaff]

    def create(self, request, *args, **kwargs):
        request.data['title'] = decrypt_data(request.data['title'])
        request.data['description'] = decrypt_data(request.data['description'])
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        for product in response.data:
            product['title'] = encrypt_data(product['title'])
            product['description'] = encrypt_data(product['description'])
        return Response(response.data)

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrStaff]

    def update(self, request, *args, **kwargs):
        request.data['title'] = decrypt_data(request.data['title'])
        request.data['description'] = decrypt_data(request.data['description'])
        return super().update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        instance.delete()


def upload_video(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        video_file = request.FILES.get('video')
        if video_file:
            # Save the uploaded file to the model
            product.video.save(video_file.name, video_file)
            
            # Enqueue the video processing task
            process_video.delay(product_id=product.id, video_file_path=product.video.path)
            
            return Response({"message": "Video upload successful, processing started."}, status=status.HTTP_202_ACCEPTED)
        return Response({"error": "No video file provided."}, status=status.HTTP_400_BAD_REQUEST)
    

class ProductPagination(pagination.PageNumberPagination):
    page_size = 1000  

class ExportProductsCSV(generics.GenericAPIView):
    permission_classes = [IsAdmin]
    pagination_class = ProductPagination

    def get(self, request, *args, **kwargs):
        paginator = self.pagination_class()
        products = Product.objects.all()
        paginated_products = paginator.paginate_queryset(products, request)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="products.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID', 'Category', 'Title', 'Description', 'Price', 'Status', 'Created At', 'Updated At'])
        for product in paginated_products:
            writer.writerow([
                product.id,
                product.category.name,
                product.title,
                product.description,
                product.price,
                product.status,
                product.created_at,
                product.updated_at
            ])
        return response