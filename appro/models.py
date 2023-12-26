import datetime
import uuid

from django.db import models
from django.utils import timezone

# Create your models here.

product_types = (("produit fini", "produit fini"), ("matière première", "matière première"))

units = (("Kg", "Kg"), ("Gr", "Gr"), ("Unité", "Unité"))


class Product(models.Model):
    img = models.ImageField(upload_to="products-images", null=True, blank=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    type_product = models.CharField(choices=product_types, max_length=255)
    qts = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    unit = models.CharField(choices=units, max_length=10, default="Kg")

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    mail = models.EmailField(null=True)
    phone = models.CharField(max_length=13, null=True)
    adress = models.TextField()

    def __str__(self):
        return self.name


class DepotGr(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True)
    qts = models.DecimalField(default=1, max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    heure = models.TimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.product.name


def generate_unique_uid():
    return uuid.uuid4().hex[:10]


class OrderGr(models.Model):
    ref = models.CharField(max_length=10, default=generate_unique_uid())
    date = models.DateField(auto_now_add=True)
    heure = models.TimeField(auto_now_add=True, null=True)


class OrderCmd(models.Model):
    ref = models.CharField(max_length=10, default=generate_unique_uid())
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now_add=True)
    heure = models.TimeField(auto_now_add=True, null=True)
    shipped = models.BooleanField(default=False)

    @property
    def get_total(self):
        lines = LineCmd.objects.filter(order=self)
        total = 0
        for item in lines:
            total += item.total_price
        return total


class LineCmd(models.Model):
    order = models.ForeignKey(OrderCmd, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qts = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    total_price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.product.name


class LivraisonGr(models.Model):
    order = models.ForeignKey(OrderGr, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qts = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.product.name


class Operation(models.Model):
    livraison = models.ForeignKey(LivraisonGr, on_delete=models.CASCADE, null=True)
    reception = models.ForeignKey(DepotGr, on_delete=models.CASCADE, null=True)
    type_operation = models.CharField(max_length=10, null=True)
    date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.livraison is None:
            self.type_operation = "sortie"
        else:
            self.type_operation = "entrée"
        super(Operation, self).save(*args, **kwargs)
