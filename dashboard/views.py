from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from cart.models import Cart
from decorator import is_admin_or_user, is_user, is_admin


@is_admin()
def view_order_details(request):
    my_order = Cart.objects.filter(is_bought=True)
    orders = set(
        my_order.values_list('order_id', 'user__email', 'payment_method', 'is_paid', 'shipping_address', 'is_send',
                             'is_delivered'))
    context = {'my_orders': orders}
    return render(request, 'dashboard/order_details.html', context)


@is_admin()
def view_order_details_ind(request, orderid):
    order_details = Cart.objects.filter(order_id=orderid)
    context = {'my_orders': order_details}
    return render(request, 'dashboard/order_detail_ind.html', context)


@is_admin()
def send_item(request, orderid):
    Cart.objects.filter(order_id=orderid).update(is_send=True)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@is_admin()
def item_delivered(request, orderid):
    Cart.objects.filter(order_id=orderid).update(is_delivered=True)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
