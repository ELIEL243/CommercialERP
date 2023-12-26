from django.urls import path
from .views import *
urlpatterns = [
    path('home-appro', ApproHomeView, name="home-appro"),
    path('product-appro', ProductApproView, name="product-appro"),
    path('supplier-appro', SupplierView, name="supplier-appro"),
    path('depot-appro', DepotGrView, name="depot-appro"),
    path('cmd-appro', OrderSupplierView, name="cmd-appro"),
    path('livraison-appro', LivraisonView, name="livraison-appro"),
    path('add-liv-appro/<str:ref>', AddOrderGr, name="add-livraison-appro"),
    path('add-cmd-appro/<str:ref>', AddCmd, name="add-order-appro"),
    path('liv-appro-det/<str:ref>', OrderApproDetail, name="liv-appro-det"),
    path('recep-cmd/<str:ref>', RecepOrderView, name="recep-cmd"),
    path('cmd-det/<str:ref>', CmdApproDetail, name="cmd-det"),
    path('edit-cmd/<str:pk>', LineCmdEdit, name="cmd-edit"),
    path('del-cmd-line/<str:pk>', DelCmdLine, name="cmd-delete"),
]