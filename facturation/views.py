import uuid
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from auth_user.decorators import allowed_users
from comm.models import OrderFact, LineItem, OrderDepot, DepotCom
from appro.models import Product
# Create your views here.


def generate_unique_uid():
    return uuid.uuid4().hex[:10]


@login_required(login_url='login')
@allowed_users(allowed_roles=['Facturation'])
def HomeFacturation(request):
    ref = generate_unique_uid()

    return render(request, 'facturation/facturation-home.html', context={'ref': ref})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Facturation'])
def FacturationView(request, ref):
    products = Product.objects.all()
    if request.user.cashier:
        order, created = OrderFact.objects.get_or_create(ref=ref, pv=request.user.cashier.pv)
    else:
        order, created = OrderFact.objects.get_or_create(ref=ref)
    lines = LineItem.objects.filter(order=order)

    if request.method == "POST":
        name = request.POST.get('name')
        qts = request.POST.get('qts')
        if Product.objects.filter(name=name).count() > 0:
            prod = Product.objects.get(name=name)
            line, created = LineItem.objects.get_or_create(order=order, product=prod)
            line.qts += int(qts)
            line.save()
            messages.success(request, "Succes")
        else:
            messages.error(request, "Echec")
    return render(request, 'facturation/add-fact.html', context={'produits': products, 'order': order, 'lines': lines, 'ref': ref})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Facturation'])
def LineEdit(request, pk):
    line = LineItem.objects.get(pk=pk)
    line.qts = int(line.qts)
    if request.method == "POST":
        qts = request.POST.get('qts')
        line.qts = int(qts)
        line.save()
        messages.success(request, "Succes!")
        return redirect('facturation-ref', ref=line.order.ref)
    return render(request, 'facturation/edit-qts.html', context={'line': line, 'ref': generate_unique_uid()})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Facturation'])
def DelLine(request, pk):
    line = LineItem.objects.get(pk=pk)
    order = line.order
    line.delete()
    messages.success(request, "Succes!")
    return redirect('facturation-ref', ref=order.ref)


@login_required(login_url='login')
@allowed_users(allowed_roles=['Facturation'])
def DetFact(request, ref):
    order = OrderFact.objects.get(ref=ref)
    order.completed = True
    order.save()
    lines = LineItem.objects.filter(order=order)
    return render(request, 'facturation/det-fact.html', context={'order': order, 'livraisons': lines, 'ref': generate_unique_uid()})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Facturation admin'])
def ReceptionPvView(request):
    depots = OrderDepot.objects.filter(pv=request.user.cashier.pv).order_by('-id')
    return render(request, 'facturation/depot-comm.html', context={'livraisons': depots, 'ref': generate_unique_uid()})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Facturation admin'])
def SalesPvView(request):
    sales = OrderFact.objects.filter(pv=request.user.cashier.pv, completed=True).order_by('-id')
    return render(request, 'facturation/sales.html', context={'livraisons': sales, 'ref': generate_unique_uid()})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Facturation admin'])
def DetailReceptionPvView(request, ref):
    order = OrderDepot.objects.get(ref=ref)
    lines = DepotCom.objects.filter(order=order)

    return render(request, 'facturation/receptions-detail.html', context={'order': order, 'livraisons': lines, 'ref': generate_unique_uid()})


@login_required(login_url='login')
@allowed_users(allowed_roles=['Facturation admin'])
def DetailSalePvView(request, ref):
    order = OrderFact.objects.get(ref=ref)
    lines = LineItem.objects.filter(order=order)

    return render(request, 'facturation/det-sale.html', context={'order': order, 'livraisons': lines, 'ref': generate_unique_uid()})
