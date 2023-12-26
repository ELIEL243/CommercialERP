import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from appro.models import Product
from auth_user.decorators import allowed_users
from prod.models import HasQts, DepotPt, Production, LivraisonProd, OperationPt, OrderProd, OrderPv, PointVente, \
    LivraisonPv


# Create your views here.


@login_required(login_url='login')
@allowed_users(allowed_roles=['Production'])
def HomeProdView(request):
    return render(request, 'prod/home-prod.html', context={})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Production'])
def ProductProdView(request):
    products = Product.objects.filter()
    if request.method == "POST":
        img = request.FILES.get('img')
        name = request.POST.get('name')
        qts = request.POST.get('qts')
        unit = request.POST.get('unit')
        if Product.objects.filter(name=name).count() > 0:
            messages.error(request, "Error")
        else:
            product = Product.objects.create(img=img, name=name, qts=qts, unit=unit, type_product="matière première")
            stock, created = HasQts.objects.get_or_create(product=product)
            stock.qts = int(qts)
            stock.save()
            messages.success(request, "Succes")
    return render(request, 'prod/products-prod.html', context={'products': products})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Production'])
def ProductionView(request):
    productions = Production.objects.all().order_by('-id')
    products = Product.objects.all()

    if request.method == "POST":
        if Product.objects.filter(name=request.POST.get('name-mp')).count() > 0 and Product.objects.filter(name=request.POST.get('name-pf')).count() > 0:
            mp = Product.objects.get(name=request.POST.get('name-mp'))
            pf = Product.objects.get(name=request.POST.get('name-pf'))
            qts_mp = request.POST.get('qts-utl')
            qts_pf = request.POST.get('qts-prod')
            Production.objects.create(product_mp=mp, product_pf=pf, qts_utl=int(qts_mp), qts_prod=int(qts_pf))
            messages.success(request, "succes !")
        else:
            messages.error(request, "error")
    return render(request, 'prod/productions.html', context={'productions': productions, 'produits': products})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Production'])
def DepotPtView(request, **kwargs):
    depots = DepotPt.objects.all().order_by('-id')
    produits = Product.objects.filter()

    if kwargs.get('type') == "appro":
        depots = DepotPt.objects.all().order_by('-id')
    elif kwargs.get('type') == "prod":
        depots = Production.objects.all().order_by('-id')
    return render(request, 'prod/depots-prod.html', context={'depots': depots, 'produits': produits})


def generate_unique_uid():
    return uuid.uuid4().hex[:10]


@login_required(login_url='login')
@allowed_users(allowed_roles=['Production'])
def LivraisonAtlView(request):
    livraisons = OrderProd.objects.all().order_by('-id')
    ref = generate_unique_uid()

    return render(request, 'prod/livraisons-prod.html', context={'livraisons': livraisons, 'ref': ref})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Production'])
def LivraisonPvView(request):
    livraisons = OrderPv.objects.all().order_by('-id')
    ref = generate_unique_uid()
    pvs = PointVente.objects.all()
    if request.GET.get('name') != "" and request.GET.get('name') is not None:
        return redirect('add-livraison-pv', ref, request.GET.get('name'))

    return render(request, 'prod/livraisons-pv.html', context={'livraisons': livraisons, 'ref': ref, 'pvs': pvs})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Production'])
def AddLivraisonAtlView(request, ref):
    products = Product.objects.filter(type_product="matière première")
    order, created = OrderProd.objects.get_or_create(ref=ref)
    lines = LivraisonProd.objects.filter(order=order)
    if request.method == "POST":
        name = request.POST.get('name')
        qts = request.POST.get('qts')
        if Product.objects.filter(name=name).count() > 0:
            prod = Product.objects.get(name=name)
            livraison, created = LivraisonProd.objects.get_or_create(order=order, product=prod)
            livraison.qts += int(qts)
            livraison.save()
            messages.success(request, "Succes")
        else:
            messages.error(request, "Echec")
    return render(request, 'prod/add-livraison-atl.html', context={'produits': products, 'livraisons': lines})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Production'])
def AddLivraisonPvView(request, ref, pv):
    products = Product.objects.filter()
    point_vente = PointVente.objects.get(name=pv)
    order = None
    lines = None
    order, created = OrderPv.objects.get_or_create(ref=ref, pv=point_vente)
    lines = LivraisonPv.objects.filter(order=order)
    if request.method == "POST":
        name = request.POST.get('name')
        qts = request.POST.get('qts')
        if Product.objects.filter(name=name).count() > 0:
            prod = Product.objects.get(name=name)
            livraison, created = LivraisonPv.objects.get_or_create(order=order, product=prod)
            livraison.qts += int(qts)
            livraison.save()
            messages.success(request, "Succes")
        else:
            messages.error(request, "Echec")
    return render(request, 'prod/add-livraison-pv.html', context={'produits': products, 'livraisons': lines, 'pv': point_vente})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Production'])
def OrderAtlDetail(request, ref):
    order = OrderProd.objects.get(ref=ref)
    lines = LivraisonProd.objects.filter(order=order)
    return render(request, 'prod/order-detail.html', context={'order': order, 'livraisons': lines})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Production'])
def OrderPvDetail(request, ref):
    order = OrderPv.objects.get(ref=ref)
    lines = LivraisonPv.objects.filter(order=order)
    return render(request, 'prod/order-pv-detail.html', context={'order': order, 'livraisons': lines})

