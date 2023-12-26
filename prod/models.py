import uuid

from django.db import models
import appro
from appro.models import Product


# Create your models here.


class HasQts(models.Model):
    product = models.OneToOneField(appro.models.Product, on_delete=models.CASCADE)
    qts = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product.name + "-" + str(self.qts)


class DepotPt(models.Model):
    product = models.ForeignKey(appro.models.Product, on_delete=models.CASCADE)
    qts = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    heure = models.TimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.product.name


class Production(models.Model):
    product_mp = models.ForeignKey(appro.models.Product, on_delete=models.CASCADE, related_name="prod_mp")
    qts_utl = models.DecimalField(default=1, max_digits=10, decimal_places=2)
    product_pf = models.ForeignKey(appro.models.Product, on_delete=models.CASCADE)
    qts_prod = models.DecimalField(default=1, max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    heure = models.TimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.product_pf.name

    def save(self, *args, **kwargs):
        stock, created = HasQts.objects.get_or_create(product=self.product_pf)
        stock.qts += self.qts_prod
        stock.save()

        super(Production, self).save(*args, **kwargs)


def generate_unique_uid():
    return uuid.uuid4().hex[:10]


class OrderProd(models.Model):
    ref = models.CharField(max_length=10, unique=True, default=generate_unique_uid)
    date = models.DateField(auto_now_add=True)
    heure = models.TimeField(auto_now_add=True, null=True)


class LivraisonProd(models.Model):
    order = models.ForeignKey(OrderProd, on_delete=models.CASCADE, default=1)
    product = models.ForeignKey(appro.models.Product, on_delete=models.CASCADE)
    qts = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.product.name

    def save(self, *args, **kwargs):
        stock, created = HasQts.objects.get_or_create(product=self.product)
        stock.qts -= self.qts
        stock.save()
        super(LivraisonProd, self).save(*args, **kwargs)


class PointVente(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class OrderPv(models.Model):
    ref = models.CharField(max_length=10, unique=True, default=generate_unique_uid)
    pv = models.ForeignKey(PointVente, on_delete=models.CASCADE, default=1)
    date = models.DateField(auto_now_add=True)
    heure = models.TimeField(auto_now_add=True, null=True)


class LivraisonPv(models.Model):
    order = models.ForeignKey(OrderPv, on_delete=models.CASCADE, default=1)
    product = models.ForeignKey(appro.models.Product, on_delete=models.CASCADE)
    qts = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product.name + "-" + str(self.qts)

    def save(self, *args, **kwargs):
        stock, created = HasQts.objects.get_or_create(product=self.product)
        stock.qts -= self.qts
        stock.save()
        super(LivraisonPv, self).save(*args, **kwargs)


class OperationPt(models.Model):
    livraison = models.ForeignKey(LivraisonProd, on_delete=models.CASCADE, null=True)
    livraison_pv = models.ForeignKey(LivraisonPv, on_delete=models.CASCADE, null=True, related_name="livraison_pv", default=1)
    reception = models.ForeignKey(DepotPt, on_delete=models.CASCADE, null=True)
    type_operation = models.CharField(max_length=10, null=True)
    date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.livraison is not None:
            self.type_operation = "sortie"
        elif self.livraison_pv is not None:
            self.type_operation = "sortie"
        else:
            self.type_operation = "entrée"
        super(OperationPt, self).save(*args, **kwargs)

