from cgitb import lookup
from posixpath import basename
from . import views
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers
from pprint import pprint

#router = SimpleRouter()
router = routers.SimpleRouter()
router.register('products', views.ProductViewSet, basename='products')

products_router = routers.NestedSimpleRouter(router, 'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product_review')
urlpatterns = router.urls + products_router.urls
# urlpatterns = [
#     path('products/', views.ProductList.as_view()),
#     path('products/<int:pk>/', views.ProductDetail.as_view())
# ] 