import datetime
from datetime import timedelta
import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Sum, F
from django.shortcuts import render
from appro.models import Product, OrderCmd
from auth_user.decorators import allowed_users
from prod.models import Production, PointVente
from comm.models import OrderFact, LineItem


# Create your views here.


@login_required(login_url='login')
#@allowed_users(allowed_roles=['Administration'])
def MainStatView(request):
    nbr_vnt_jr = OrderFact.objects.filter(date=datetime.datetime.today()).count()
    most_sellings_product = Product.objects.annotate(total_count=Count('lineitem__id'), total_sale=Sum(F('lineitem__qts') * F('price'))).order_by('-total_count')
    recent_sales = OrderFact.objects.filter(completed=True).order_by('-id')[:10]
    nbr_prod = Product.objects.all().count()
    nbr_pv = PointVente.objects.all().count()
    nbr_utl = User.objects.all().count()
    ventes = OrderFact.objects.filter(date=datetime.datetime.today(), completed=True)
    for i in OrderFact.objects.filter(completed=True):
        i.date = i.date.replace(month=12)
        i.save()
    ventes_month = OrderFact.objects.filter(date__month=datetime.datetime.today().month, completed=True)
    vnt_mth_data = []
    vnt_mth_labels = []
    vnt_jr_data = []
    vnt_jr_labels = []
    dates = []
    cpt = 0
    for item in ventes_month:
        if item.date not in vnt_mth_labels:
            vnt_mth_labels += [item.date]
    for date in vnt_mth_labels:
        total = 0
        for item in ventes_month.filter(date=date):
            total += item.get_total
        vnt_mth_data += [total]

    for item in ventes:
        if item.pv.name not in vnt_jr_labels:
            vnt_jr_labels += [item.pv.name]
    for pv in vnt_jr_labels:
        total = 0
        for item in ventes.filter(pv__name=pv):
            total += item.get_total
        vnt_jr_data += [total]
    nbr_prod_jr = Production.objects.filter(date=datetime.datetime.today()).count()
    nbr_cmd_jr = OrderCmd.objects.filter(date=datetime.datetime.today(), shipped=True).count()
    nbr_chf_aff = 0
    for item in ventes:
        nbr_chf_aff += item.get_total
    return render(request, 'reporting/main-dashboard.html',
                  context={'nbr_vnt_jr': nbr_vnt_jr, 'chf_aff': nbr_chf_aff,
                           'nbr_prod_jr': nbr_prod_jr, 'nbr_cmd_jr': nbr_cmd_jr,
                           'vnt_mth_data': vnt_mth_data, 'vnt_mth_labels': vnt_mth_labels,
                           'ventes_mth': ventes_month, 'vnt_jr_labels': vnt_jr_labels,
                           'vnt_jr_data': vnt_jr_data, 'nbr_prod': nbr_prod,
                           'nbr_pv': nbr_pv, 'nbr_utl': nbr_utl, 'top_products': most_sellings_product,
                           'recent_sales': recent_sales})
