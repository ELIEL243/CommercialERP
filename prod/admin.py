from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(PointVente)
admin.site.register(OrderPv)
admin.site.register(OrderProd)
admin.site.register(LivraisonProd)
admin.site.register(LivraisonPv)
admin.site.register(Production)
admin.site.register(DepotPt)