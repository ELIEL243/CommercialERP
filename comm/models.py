from django.contrib.auth.models import User
from django.db import models

from appro.models import Product
from prod.models import PointVente


# Create your models here.


class HasQtsCom(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    qts = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    pv = models.ForeignKey(PointVente, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name + "-" + str(self.qts)


class OrderDepot(models.Model):
    ref = models.CharField(max_length=10)
    pv = models.ForeignKey(PointVente, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    heure = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.ref + "-" + self.pv.name


class DepotCom(models.Model):
    order = models.ForeignKey(OrderDepot, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qts = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product.name


class OrderFact(models.Model):
    ref = models.CharField(max_length=10, null=True)
    pv = models.ForeignKey(PointVente, on_delete=models.CASCADE, null=True)
    completed = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)
    heure = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.ref + "-" + self.pv.name

    @property
    def get_total(self):
        lines = LineItem.objects.filter(order=self)
        total = 0
        for item in lines:
            total += item.qts * item.product.price
        return int(total)


class LineItem(models.Model):
    order = models.ForeignKey(OrderFact, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qts = models.DecimalField(default=0, max_digits=10, decimal_places=2)

    def __str__(self):
        return self.order.ref + "-" + self.product.name

    @property
    def get_total(self):
        return self.product.price * self.qts


class Cashier(models.Model):
    name = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pv = models.ForeignKey(PointVente, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + "-" + self.pv.name
