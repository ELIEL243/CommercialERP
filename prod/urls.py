from django.urls import path
from .views import *
urlpatterns = [
    path('home-prod', HomeProdView, name="home-prod"),
    path('productions', ProductionView, name="production"),
    path('products-prod', ProductProdView, name="products-prod"),
    path('reception-prod', DepotPtView, name="reception-prod"),
    path('reception-prod/<str:type>', DepotPtView, name="reception-prod-type"),
    path('livraisons-atl-prod/', LivraisonAtlView, name="livraison-atl"),
    path('livraisons-pv-prod/', LivraisonPvView, name="livraison-pv"),
    path('add-liv-atl/<str:ref>', AddLivraisonAtlView, name="add-livraison-atl"),
    path('add-liv-pv/<str:ref>/<str:pv>', AddLivraisonPvView, name="add-livraison-pv"),
    path('det-liv-atl/<str:ref>', OrderAtlDetail, name="livraison-det-atl"),
    path('det-liv-pv/<str:ref>', OrderPvDetail, name="livraison-det-pv"),
]