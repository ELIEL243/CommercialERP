from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Product)
admin.site.register(DepotGr)
admin.site.register(LivraisonGr)
admin.site.register(Operation)
admin.site.register(OrderGr)
admin.site.register(OrderCmd)