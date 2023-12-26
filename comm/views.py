from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from appro.models import Product
from auth_user.decorators import allowed_users
from comm.models import OrderDepot, DepotCom, OrderFact, LineItem
from prod.models import PointVente


# Create your views here.

@login_required(login_url='login')
@allowed_users(allowed_roles=['Commercialisation'])
def ComeHomeView(request):
    return render(request, 'comm/home-comm.html', context={})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Commercialisation'])
def ProductComView(request):
    products = Product.objects.filter()

    return render(request, 'comm/products.html', context={'products': products})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Commercialisation'])
def ProductDetailView(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == "POST":
        price = request.POST.get('price')
        product = Product.objects.get(id=pk)
        product.price = int(price)
        product.save()
        messages.success(request, "Succes")
        return redirect('product-comm')

    return render(request, 'comm/product-detail.html', context={'product': product})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Commercialisation'])
def PointVenteView(request):
    pvs = PointVente.objects.all()
    if request.method == "POST":
        name = request.POST.get('name')
        address = request.POST.get('address')
        PointVente.objects.create(name=name, address=address)
        messages.success(request, "good")
    return render(request, 'comm/point-vente.html', context={'pvs': pvs})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Commercialisation'])
def ReceptionPvView(request):
    depots = OrderDepot.objects.all().order_by('-id')
    return render(request, 'comm/depot-comm.html', context={'livraisons': depots})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Commercialisation'])
def SalesPvView(request):
    sales = OrderFact.objects.all().order_by('-id')
    return render(request, 'comm/sales.html', context={'livraisons': sales})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Commercialisation'])
def DetailReceptionPvView(request, ref):
    order = OrderDepot.objects.get(ref=ref)
    lines = DepotCom.objects.filter(order=order)

    return render(request, 'comm/receptions-detail.html', context={'order': order, 'livraisons': lines})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Commercialisation'])
def DetailSalePvView(request, ref):
    order = OrderFact.objects.get(ref=ref)
    lines = LineItem.objects.filter(order=order)

    return render(request, 'comm/det-sale.html', context={'order': order, 'livraisons': lines})
