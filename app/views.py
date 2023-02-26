import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from .models import Item, ItemsInOrder, Order


def item_list(request):
    items = Item.objects.all()
    context = {'items': items}
    return render(request, 'item_list.html', context)


def item_detail(request, pk):
    item = get_object_or_404(Item, id=pk)
    in_order = False
    quantity = 0
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, paid=False).first()
        if order:
            items_in_order = ItemsInOrder.objects.filter(order=order)
            for item_in_order in items_in_order:
                if item_in_order.item.id == item.id:
                    in_order = True
                    quantity = item_in_order.quantity
    context = {
        'item': item,
        'in_order': in_order,
        'quantity': quantity,
        'order': order,
    }
    return render(request, 'item_detail.html', context)


@login_required
def orders_list(request):
    orders = Order.objects.filter(user=request.user)
    context = {'orders': orders}
    return render(request, 'orders_list.html', context)


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, id=pk, user=request.user)
    items_in_order = ItemsInOrder.objects.filter(order=order)
    context = {
        'order': order,
        'items_in_order': items_in_order,
    }
    if request.user != order.user:
        return redirect('app:orders_list')
    return render(request, 'order_detail.html', context)


@login_required
def add_to_order(request, pk):
    item = get_object_or_404(Item, id=pk)
    unpaid_order = Order.objects.filter(user=request.user, paid=False)
    if unpaid_order.exists():
        order = unpaid_order.first()
    else:
        order = Order.objects.create(user=request.user)
        request.session['order_id'] = order.id
    order_item, created = ItemsInOrder.objects.get_or_create(
        order=order,
        item=item,
    )
    if not created:
        order_item.quantity += 1
        order_item.save()
    else:
        order.items.add(item)
        order.save()
    return redirect(request.META.get('HTTP_REFERER', 'app:item_detail'))


@login_required
def delete_from_order(request, pk):
    item = get_object_or_404(Item, id=pk)
    order = Order.objects.get(user=request.user, paid=False)
    order_item = ItemsInOrder.objects.get(order=order, item=item)
    if order_item.quantity > 1:
        order_item.quantity -= 1
        order_item.save()
    else:
        order_item.delete()
        if not order.items.exists():
            order.delete()
            return redirect('app:orders_list')
    return redirect(request.META.get('HTTP_REFERER', 'app:order_detail'))


def stripe_session(request, order):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    tax = stripe.TaxRate.create(
        display_name="Sales Tax",
        inclusive=False,
        percentage=settings.TAX_VALUE,
        country="US",
        state="CA",
        jurisdiction="US - CA",
        description="CA Sales Tax",
    )
    checkout_session = stripe.checkout.Session.create(
        customer_email=request.user.email,
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'unit_amount': int(i.item.price * 100),
                    'currency': 'usd',
                    'product_data': {
                        'name': i.item.name,
                        'description': i.item.description,
                    },
                },
                'tax_rates': [tax.id],
                'quantity': i.quantity,
            } for i in order.itemsinorder_set.all()],
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('app:success', kwargs={'pk': order.id})),
        cancel_url=request.build_absolute_uri(reverse('app:cancel')),
    )

    order.stripe_session_id = checkout_session.id
    order.save()
    return checkout_session


# @csrf_exempt
# def buy_item(request, pk):
#     item = get_object_or_404(Item, id=pk)
#     if request.user.is_authenticated:
#         order = Order.objects.create(user=request.user)
#         order.items.add(item)
#         order.total_price = item.price
#         order.save()
#         checkout_session = stripe_session(request, order)
#         return redirect(checkout_session.url)
#     else:
#         return redirect('users:login')


@csrf_exempt
def pay_for_order(request, pk):
    order = get_object_or_404(Order, user=request.user, id=pk)
    order.total_price = order.get_total_cost()
    order.save()
    if request.user.is_authenticated:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        checkout_session = stripe_session(request, order)
        return redirect(checkout_session.url)
    else:
        return redirect('users:login')


class SuccessView(TemplateView):
    template_name = 'success.html'

    def get(self, request, pk):
        order = Order.objects.get(pk=pk)
        session = stripe.checkout.Session.retrieve(order.stripe_session_id)
        if session.status == 'complete':
            order.paid = True
            order.save()
            return render(request, self.template_name)


class CancelView(TemplateView):
    template_name = 'cancel.html'
