from django.core.exceptions import BadRequest
from django.db.models import F, Q, Sum
from django.shortcuts import render, HttpResponse, redirect
from django.http import Http404, HttpResponseRedirect
# Create your views here.
from cart.models import Cart
from decorator import is_admin, is_admin_or_user, is_user
from products.models import Product
import uuid
import requests as req


def home(request):
    context = {
        'trending_products': Product.objects.filter(is_available=True).filter(stock__gt=0).order_by('-total_click')[:4],
        'latest_products': Product.objects.filter(is_available=True).filter(stock__gt=0).order_by('-create_date')[:4],
    }
    return render(request, 'home/home.html', context)


def product_desc(request, pk):
    context = {}
    try:
        product = Product.objects.get(pk=pk)
        context['product'] = product
    except:
        raise Http404
    return render(request, 'home/product_desc.html', context)


@is_admin_or_user()
def add_to_cart(request):
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        product_id = request.POST['product_id']
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise BadRequest('Invalid request.')

        if product.stock > 0:
            cart_product = Cart.objects.filter(user=request.user).filter(product_id=product_id).filter(is_bought=False)
            if cart_product.exists():
                cart_product.update(quantity=quantity)
            else:
                Cart.objects.create(
                    user=request.user,
                    product_id=product_id,
                    is_bought=False,
                    quantity=quantity
                )
        else:
            return HttpResponse('product out of stock')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@is_admin_or_user()
def remove_cart(request):
    if request.method == 'POST':
        Cart.objects.filter(pk=request.POST['pk']).delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponse('Bad Request')


@is_admin_or_user()
def show_cart(request):
    my_cart = Cart.objects.filter(user=request.user).filter(is_bought=False)
    price = 0
    for cart in my_cart:
        price = price + cart.price
    context = {'my_cart': my_cart, 'price': price}
    return render(request, 'home/cart.html', context)


@is_admin_or_user()
def add_subtract_cart_item(request):
    if request.method == 'POST':
        cart = Cart.objects.filter(pk=request.POST['pk']).filter(user=request.user).get(is_bought=False)
        product_stock = cart.product.stock
        if int(request.POST['asci']) == 0:
            if cart.quantity == 1:
                cart.delete()
            else:
                cart_item = Cart.objects.filter(pk=request.POST['pk']).filter(user=request.user).get(is_bought=False)
                cart_item.quantity = cart_item.quantity - 1
                cart_item.save()
        elif int(request.POST['asci']) == 1:
            if product_stock > 0:

                cart_item = Cart.objects.filter(pk=request.POST['pk']).filter(user=request.user).get(is_bought=False)
                cart_item.quantity = cart_item.quantity + 1
                cart_item.save()
            else:
                return HttpResponse('product out of stock')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@is_admin_or_user()
def checkout(request):
    if request.method == 'POST':
        uuid_str = str(uuid.uuid4().hex)
        cart_item = Cart.objects.filter(user=request.user).filter(is_bought=False)
        cart_item.update(
            order_id=uuid_str,
            shipping_address=request.POST['shipping_address'],
            payment_method=request.POST['payment_method'],
        )
        if request.POST['payment_method'] == 'Cash On Delivery':
            cart_item.update(is_bought=True)
        if request.POST['payment_method'] == 'Esewa':
            my_cart = Cart.objects.filter(user=request.user).filter(is_bought=False)
            price = 0
            for cart in my_cart:
                price = price + cart.price
            return redirect('home:esewa_pay', orderid=uuid_str, price=price)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@is_admin_or_user()
def esewa_pay(request, orderid, price):
    context = {'orderid': orderid, 'price': price}
    return render(request, 'home/esewa.html', context)


@is_admin_or_user()
def esewa_faliure(request):
    return redirect('home:show_cart')


def esewa_success(request):
    import xml.etree.ElementTree as ET
    data = request.GET.copy()
    url = "https://uat.esewa.com.np/epay/transrec"
    d = {
        'amt': data['amt'],
        'scd': 'EPAYTEST',
        'rid': data['refId'],
        'pid': data['oid'],
    }
    resp = req.post(url, d)
    root = ET.fromstring(resp.content)
    status = root[0].text.strip()
    if status == 'Success':
        Cart.objects.filter(
            order_id=data['oid']
        ).update(
            is_bought=True,
            is_paid=True
        )
        return redirect('home:my_order')
    else:
        return HttpResponse('failure')


@is_admin_or_user()
def my_order(request):
    my_order = Cart.objects.filter(user=request.user).filter(is_bought=True)
    rewards_point = my_order.aggregate(Total=(Sum('price') / 1000))['Total']
    print(my_order.aggregate(Total=(Sum('price'))))
    orders = set(
        my_order.values_list('order_id', 'payment_method', 'is_paid', 'shipping_address', 'is_send', 'is_delivered'))
    context = {'my_orders': orders, 'rewards_point': rewards_point}
    return render(request, 'home/my_order.html', context)


@is_admin_or_user()
def view_order_details(request, orderid):
    order_details = Cart.objects.filter(order_id=orderid).filter(user=request.user)
    context = {'my_orders': order_details}
    return render(request, 'home/order_details.html', context)


def search(request):
    if request.method == 'GET':
        query = request.GET['search']
        product = Product.objects.filter(Q(name__contains=query) | Q(categories__name__contains=query)).filter(
            is_available=True).filter(stock__gt=0).order_by('-total_click')
        context = {}

        try:
            season = request.GET['season']
            if season:
                product = product.filter(season__name=season)


        except:
            season = ''
        try:
            price = request.GET["price"]
            product = product.filter(price__lte=price)
            context['price'] = price
        except:
            context['price'] = ''
            pass
        context['search'] = query
        context['products'] = product
        context['season'] = season

        return render(request, 'home/search.html', context)


def view_all_product(request):
    context = {
        'products': Product.objects.filter(is_available=True).filter(stock__gt=0).order_by('-create_date'),
    }
    return render(request, 'home/all_product.html', context)

def view_customer_product(request):
    context = {
        'products': Product.objects.filter(is_available=True).filter(user__is_admin=False).filter(stock__gt=0).order_by('-create_date'),
    }
    return render(request, 'home/all_product.html', context)

@is_admin_or_user()
def esewa_failure(request):
    return redirect('home:show_cart')


