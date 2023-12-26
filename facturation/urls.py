from django.urls import path
from .views import *

urlpatterns = [
    path('home-facturation/', HomeFacturation, name="home-facturation"),
    path('facturation/<str:ref>/', FacturationView, name="facturation-ref"),
    path('edit-qts/<str:pk>/', LineEdit, name="line-edit"),
    path('del-line/<str:pk>/', DelLine, name="line-del"),
    path('det-fact/<str:ref>/', DetFact, name="line-det"),
    path('recep-pv2/', ReceptionPvView, name="recep-pv-fact"),
    path('sales-pv2/', SalesPvView, name="sales-pv-fact"),
    path('recep-pv2/<str:ref>', DetailReceptionPvView, name="reception-det-pv-fact"),
    path('sales-pv2/<str:ref>', DetailSalePvView, name="sale-detail-fact"),
]