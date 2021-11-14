from django.shortcuts import render
from .models import Seller, Item, OldItem
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.db.utils import IntegrityError

# Create your views here.


def home(request):
    return render(request, 'shophaul/index.html')


def products(request):
    return render(request, 'shophaul/products.html')


def top_products(request):
    item_query = Item.objects.all().order_by('-quantity')[:10]
    items_json = item_query.values_list()
    items_json = json.dumps(list(items_json), cls=DjangoJSONEncoder)
    if item_query.count() > 0:
        return render(request, 'shophaul/top_products.html', {'items': item_query, 'itm': items_json})
    return render(request, 'shophaul/top_products.html', {'message': "No Products to show"})


# def top_sellers(request):
#     top = TopSellers.objects.all()
#     top_json = top.values_list()
#     top_json = json.dumps(list(top), cls=DjangoJSONEncoder)
#     if top.count() > 0:
#         return render(request, 'shophaul/top_sellers.html', {'items': top, 'itm': top_json})
#     return render(request, 'shophaul/top_sellers.html', {'message': "No Sellers to show"})


@login_required
def my_products(request):
    current_seller = Seller.objects.get(user=request.user)
    item_query = Item.objects.filter(seller=current_seller)
    items_json = item_query.values_list()
    items_json = json.dumps(list(items_json), cls=DjangoJSONEncoder)
    if item_query.count() > 0:
        return render(request, 'shophaul/myproducts.html', {'items': item_query, 'itm': items_json})
    return render(request, 'shophaul/myproducts.html', {'message': "No Product to show"})


@csrf_exempt
@login_required
def add_update_product(request):
    current_seller = Seller.objects.get(user=request.user)
    item_query = Item.objects.filter(seller=current_seller)
    # topseller_query = TopSellers.objects.filter(seller=current_seller)
    if request.method == "GET":
        items_json = item_query.values_list()
        items_json = json.dumps(list(items_json), cls=DjangoJSONEncoder)
        if item_query.count() > 0:
            return render(request, 'shophaul/add_update_product.html', {'items': item_query, 'itm': items_json})
        return render(request, 'shophaul/add_update_product.html', {'message': "No Product to show"})
    elif request.method == 'POST':
        try:
            name = request.POST.get('name')
            quantity = request.POST.get('quantity')
            price = request.POST.get('price')
            address = request.POST.get('address')
        except Exception as exc:
            return JsonResponse({'status': str(exc)})
        try:

            item = Item.objects.get(name=name, seller=current_seller)
            # old_price = item.price
            # old_quantity = item.quantity
            item.address = address
            item.price = price
            item.quantity = quantity
            item.save()
            oitem = OldItem.objects.create(
                oname=name, oprice=price, oquantity=quantity, oaddress=address, oseller=current_seller
            )
            oitem.save()
            # top = TopSellers.objects.get(topseller=current_seller)
            # top.topprice = top.topprice + \
            #     (price*quantity) - (old_price*old_quantity)
            # top.save()
        except Exception as exc:
            return JsonResponse({'status': str(exc)})

        return JsonResponse({'status': 'Success'})
    else:
        JsonResponse({'status': 'Bad Request'})


@csrf_exempt
@require_POST
def add_product(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'Bad Request'})
    try:
        current_seller = Seller.objects.get(user=request.user)
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        address = request.POST.get('address')
    except Exception as exc:
        return JsonResponse({'status': str(exc)})
    try:
        item = Item.objects.create(
            name=name, price=price, quantity=quantity, address=address, seller=current_seller)
        item.save()
        oitem = OldItem.objects.create(
            oname=name, oprice=price, oquantity=quantity, oaddress=address, oseller=current_seller
        )
        oitem.save()
        # top = TopSellers.objects.create(
        #     topseller_name=current_seller.user, topprice=price*quantity,  top_seller=current_seller
        # )
        # top.save()

        print("saved")
    except IntegrityError:
        return JsonResponse({'status': "An Item with Same Name Already Exists"})
    return JsonResponse({'status': 'Success'})


@csrf_exempt
@require_POST
def delete_product(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'Bad Request'})
    try:
        current_seller = Seller.objects.get(user=request.user)
        name = request.POST.get('name')
        item = Item.objects.get(name=name)
        item.delete()
    except Exception as exc:
        return JsonResponse({'status': str(exc)})
    return JsonResponse({'status': 'Success'})


@login_required
def previous_products(request):
    current_seller = Seller.objects.get(user=request.user)
    item_query = OldItem.objects.filter(oseller=current_seller)
    items_json = item_query.values_list()
    items_json = json.dumps(list(items_json), cls=DjangoJSONEncoder)
    if item_query.count() > 0:
        return render(request, 'shophaul/previous_products.html', {'items': item_query, 'itm': items_json})
    return render(request, 'shophaul/previous_products.html', {'message': "No Product to show"})
