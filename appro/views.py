import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from auth_user.decorators import allowed_users
from django.shortcuts import render, redirect

from appro.models import Product, DepotGr, LivraisonGr, Operation, OrderGr, Supplier, OrderCmd, LineCmd
from prod.models import HasQts, DepotPt, OperationPt


# Create your views here.


@login_required(login_url='login')
@allowed_users(allowed_roles=['Approvisionnement'])
def ApproHomeView(request):
    return render(request, 'appro/home-appro.html', context={})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Approvisionnement'])
def ProductApproView(request):
    products = Product.objects.filter(type_product="matière première")
    if request.method == "POST":
        img = request.FILES.get('img')
        name = request.POST.get('name')
        qts = request.POST.get('qts')
        unit = request.POST.get('unit')
        if Product.objects.filter(name=name).count() > 0:
            messages.error(request, "Error")
        else:
            Product.objects.create(img=img, name=name, qts=qts, unit=unit, type_product="matière première")
            messages.success(request, "Succes")
    return render(request, 'appro/products.html', context={'products': products})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Approvisionnement'])
def SupplierView(request):
    suppliers = Supplier.objects.all()

    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        mail = request.POST.get('mail')
        address = request.POST.get('address')

        if suppliers.filter(name=name).count() > 0:
            messages.error(request, "Error")
        else:
            Supplier.objects.create(name=name, mail=mail, phone=phone, adress=address)
            messages.success(request, "Succes !")
    return render(request, 'appro/suppliers.html', context={'suppliers': suppliers})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Approvisionnement'])
def DepotGrView(request):
    depots = DepotGr.objects.all().order_by('-id')
    produits = Product.objects.filter(type_product='matière première')
    suppliers = Supplier.objects.all()

    if request.method == "POST":
        name = request.POST.get('name')
        qts = request.POST.get('qts')
        price = request.POST.get('price')
        supplier = Supplier.objects.get(name=request.POST.get('supplier'))
        if Product.objects.filter(name=name).count() > 0:
            prod = Product.objects.get(name=name)
            depot = DepotGr.objects.create(product=prod, qts=qts, price=price, supplier=supplier)
            prod.qts += int(qts)
            prod.save()
            Operation.objects.create(reception=depot)
            messages.success(request, "Succes")
        else:
            messages.error(request, "Echec")
    return render(request, 'appro/depots.html', context={'depots': depots, 'produits': produits, 'suppliers': suppliers})


def generate_unique_uid():
    return uuid.uuid4().hex[:10]


@login_required(login_url='login')
@allowed_users(allowed_roles=['Approvisionnement'])
def LivraisonView(request):
    livraisons = OrderGr.objects.all().order_by('-id')
    ref = generate_unique_uid()
    return render(request, 'appro/livraisons.html', context={'livraisons': livraisons, 'ref': ref})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Approvisionnement'])
def OrderSupplierView(request):
    orders = OrderCmd.objects.all().order_by('-id')
    ref = generate_unique_uid()
    return render(request, 'appro/orders.html', context={'orders': orders, 'ref': ref})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Approvisionnement'])
def RecepOrderView(request, ref):
    order = OrderCmd.objects.get(ref=ref)
    lines = LineCmd.objects.filter(order=order)
    order.shipped = True
    order.save()
    for line in lines:
        DepotGr.objects.create(product=line.product, qts=line.qts, price=line.total_price, supplier=order.supplier)
    return redirect('cmd-appro')


@login_required(login_url='login')
@allowed_users(allowed_roles=['Approvisionnement'])
def AddCmd(request, ref):
    products = Product.objects.all()
    order, created = OrderCmd.objects.get_or_create(ref=ref)
    lines = LineCmd.objects.filter(order=order)
    suppliers = Supplier.objects.all()
    if request.method == "POST":
        name = request.POST.get('name')
        supplier_name = request.POST.get('supplier')
        order.supplier = Supplier.objects.get(name=supplier_name)
        order.save()
        total_price = request.POST.get('total-price')
        qts = request.POST.get('qts')

        if Product.objects.filter(name=name).count() > 0:
            prod = Product.objects.get(name=name)
            line, created = LineCmd.objects.get_or_create(order=order, product=prod, total_price=total_price)
            line.qts += int(qts)
            line.save()
            messages.success(request, "Succes")
        else:
            messages.error(request, "Echec")

    return render(request, 'appro/add-cmd-prod.html',
                  context={'orders': lines, 'produits': products, 'order': order, 'suppliers': suppliers})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Approvisionnement'])
def AddOrderGr(request, ref):
    products = Product.objects.filter(type_product="matière première")
    order, created = OrderGr.objects.get_or_create(ref=ref)
    lines = LivraisonGr.objects.filter(order=order)
    if request.method == "POST":
        name = request.POST.get('name')
        qts = request.POST.get('qts')
        if Product.objects.filter(name=name).count() > 0:
            prod = Product.objects.get(name=name)
            livraison, created = LivraisonGr.objects.get_or_create(order=order, product=prod)
            livraison.qts += int(qts)
            livraison.save()
            prod.qts -= int(qts)
            prod.save()
            stock, created = HasQts.objects.get_or_create(product=prod)
            stock.qts += int(qts)
            stock.save()

            stock = DepotPt.objects.create(product=prod, qts=qts)
            stock.save()
            messages.success(request, "Succes")
        else:
            messages.error(request, "Echec")

    return render(request, 'appro/add-liv-prod.html', context={'livraisons': lines, 'produits': products, 'order': order})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Approvisionnement'])
def OrderApproDetail(request, ref):
    order = OrderGr.objects.get(ref=ref)
    lines = LivraisonGr.objects.filter(order=order)
    return render(request, 'appro/liv-det-prod.html', context={'order': order, 'livraisons': lines})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Approvisionnement'])
def CmdApproDetail(request, ref):
    order = OrderCmd.objects.get(ref=ref)
    lines = LineCmd.objects.filter(order=order)
    return render(request, 'appro/cmd-det.html', context={'order': order, 'orders': lines})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Approvisionnement'])
def LineCmdEdit(request, pk):
    line = LineCmd.objects.get(pk=pk)
    line.qts = int(line.qts)
    line.total_price = int(line.total_price)
    if request.method == "POST":
        qts = request.POST.get('qts')
        price = request.POST.get('price')
        line.qts = int(qts)
        line.total_price = int(price)
        line.save()
        messages.success(request, "Succes!")
        return redirect('add-order-appro', ref=line.order.ref)
    return render(request, 'appro/edit-price.html', context={'line': line, 'ref': generate_unique_uid()})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Approvisionnement'])
def DelCmdLine(request, pk):
    line = LineCmd.objects.get(pk=pk)
    order = line.order
    line.delete()
    messages.success(request, "Succes!")
    return redirect('add-order-appro', ref=order.ref)
