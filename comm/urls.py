from django.urls import path
from .views import *
urlpatterns = [
    path('home-comm/', ComeHomeView, name="home-comm"),
    path('product-comm/', ProductComView, name="product-comm"),
    path('product-det/<str:pk>', ProductDetailView, name="product-detail"),
    path('point-ventes/', PointVenteView, name="pv-comm"),
    path('recep-pv/', ReceptionPvView, name="recep-pv"),
    path('sales-pv/', SalesPvView, name="sales-pv"),
    path('recep-pv/<str:ref>', DetailReceptionPvView, name="reception-det-pv"),
    path('sales-pv/<str:ref>', DetailSalePvView, name="sale-detail"),
]