from rest_framework import generics
from rest_framework.response import Response
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .permissions import IsAdminOrStaff, IsAdmin
from .utils import encrypt_data, decrypt_data

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
