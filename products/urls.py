from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import  CategoryListCreateView, CategoryDetailView, ProductListCreateView, ProductDetailView, ExportProductsCSV, upload_video

urlpatterns = [
    # Your other URLs here
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

    path('upload/video/<int:product_id>/', upload_video, name='upload-video'),
    path('export/products/csv/', ExportProductsCSV.as_view(), name='export-products-csv'),

]
