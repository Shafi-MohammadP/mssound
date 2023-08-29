from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from checkout.models import Order, OrderItem, Orderstatus, Itemstatus
from userprofile.models import Address
from variant.models import Variant, VariantImage
from cart.models import Cart
from django.contrib import messages
from user.models import User
from django.contrib import messages
from userprofile.models import Wallet
# Create your views here.


def order_list(request):
    user = request.user
    order = Order.objects.all()
    context = {
        'order': order,
    }

    return render(request, 'dashboard/order.html', context)


def viewOrder(request, view_id):

    try:
        orderview = Order.objects.get(id=view_id)
        address = Address.objects.get(id=orderview.address.id)
        products = OrderItem.objects.filter(order=view_id)
        variant_ids = [product.variant.id for product in products]
        image = VariantImage.objects.filter(
            variant__id__in=variant_ids).distinct('variant__color')
        item_status_o = Itemstatus.objects.all()
        context = {
            'orderview': orderview,
            'address': address,
            'products': products,
            'image': image,
            'item_status_o': item_status_o
        }

        return render(request, 'View/order_view.html', context)
    except Order.DoesNotExist:
        print("Order does not exist")
    except Address.DoesNotExist:
        print("Address does not exist")
    return redirect('order_list')


def change_status(request):

    if not request.user.is_authenticated:
        return redirect('admin_login1')

    orderitem_id = request.POST.get('orderitem_id')
    order_status = request.POST.get('status')
    order_variant = request.POST.get('variant_id')

    orderitems = OrderItem.objects.get(variant=order_variant, id=orderitem_id)
    item_status_instance = Itemstatus.objects.get(id=order_status)

    orderitems.orderitem_status = item_status_instance
    orderitems.save()
    view_id = orderitems.order.id

    all_order_items = OrderItem.objects.filter(order=view_id)
    print(all_order_items, '11111111111111111111111111111111111111')
    Pending = 0
    Processing = 0
    Shipped = 0
    Delivered = 0
    Cancelled = 0
    Return = 0

    for i in all_order_items:
        # Pending
        if i.orderitem_status.id == 1:
            Pending += 1
        # Processing
        if i.orderitem_status.id == 2:
            Processing += 1
        # Shipped

        if i.orderitem_status.id == 3:
            Shipped += 1
        # Delivered
        if i.orderitem_status.id == 4:
            Delivered += 1
        # Cancelled
        if i.orderitem_status.id == 5:
            Cancelled += 1
        # Return
        if i.orderitem_status.id == 6:
            Return += 1

    total_items = len(all_order_items)
    print(total_items, '65555555555555555555555555555555555555555')

    total_value = 1
    if total_items == Pending:
        total_value = 1
    elif total_items == Processing:
        total_value = 2
    elif total_items == Shipped:
        total_value = 3
    elif total_items == Delivered:
        total_value = 4
    elif total_items == Cancelled:
        total_value = 5
    elif total_items == Return:
        total_value = 6

    change_all_items_status = Order.objects.get(id=view_id)
    item_status_instance_all = Orderstatus.objects.get(id=total_value)
    change_all_items_status.order_status = item_status_instance_all
    change_all_items_status.save()

    messages.success(request, 'status updated')
    return redirect('order_list')


def cancel_order(request, cancel_id):
    try:
        orderitem_id = OrderItem.objects.get(id=cancel_id)
        orderitem = orderitem_id
        view_id = orderitem_id.order.id
    except:
        return redirect('userprofile')

    if request.method == 'POST':
        option = request.POST.get('options')
        reason = request.POST.get('reason')

        if option.strip() == '':
            messages.error(request, "enter your options")
            return redirect('order_detail', view_id)

        if reason.strip() == '':
            messages.error(request, "Enter Your Reason")
            return redirect('order_detail', view_id)

        order = Order.objects.filter(id=view_id).first()
        qty = orderitem.quantity
        variant_id = orderitem.variant.id
        variant = Variant.objects.filter(id=variant_id).first()

        if order.payment_mode == 'Razorpay' or order.payment_mode == 'Wallet':
            order = Order.objects.get(id=view_id)
            total_price = order.total_price

            try:
                wallet = Wallet.objects.get(user=request.user)
                wallet.wallet += total_price
                wallet.save()
            except wallet.DoesNotExist:
                wallet = Wallet.objects.create(
                    user=request.user, wallet=total_price)

        variant.quantity = variant.quantity + qty
        variant.save()
        order_item_id = Itemstatus.objects.get(id=5)
        orderitem.orderitem_status = order_item_id
        orderitem.save()

        try:
            # total item_status
            all_order_item = OrderItem.objects.filter(order=view_id)

            # import pdb
            # pdb.set_trace()
            total_count = all_order_item.count()

            Pending = all_order_item.filter(orderitem_status__id=1).count()
            Processing = all_order_item.filter(orderitem_status__id=2).count()
            Shipped = all_order_item.filter(orderitem_status__id=3).count()
            Delivered = all_order_item.filter(orderitem_status__id=4).count()
            Cancelled = all_order_item.filter(orderitem_status__id=5).count()
            Return = all_order_item.filter(orderitem_status__id=6).count()

            if total_count == Pending:
                total_value = 1
            elif total_count == Processing:
                total_value = 2
            elif total_count == Shipped:
                total_value = 3
            elif total_count == Delivered:
                total_value = 4
            elif total_count == Cancelled:
                total_value = 5
            elif total_count == Return:
                total_value = 6
            else:
                total_value = 1

        except:
            return redirect('order_view', view_id)

        change_all_item_status = Order.objects.get(id=view_id)
        item_status_instance_all = Orderstatus.objects.get(id=total_value)
        change_all_item_status.order_status = item_status_instance_all
        change_all_item_status.save()

        messages.success(request, 'Your Order Cancelled Succesfully')

        return redirect('order_detail', view_id)


def return_order(request, return_id):

    try:
        orderitem_id = OrderItem.objects.get(id=return_id)
        view_id = orderitem_id.order.id
    except:
        return redirect('userprofile')

    if request.method == 'POST':
        options = request.POST.get('options')
        reason = request.POST.get('reason')

        if options.strip() == '' or reason.strip() == '':
            messages.error(request, 'Field cannot be empty')
            return redirect('order_detail', view_id)

        qty = orderitem_id.quantity
        variant_id = orderitem_id.variant.id
        order_id = Order.objects.get(id=orderitem_id.order.id)

        variant = Variant.objects.filter(id=variant_id).first()
        variant.quantity = variant.quantity + qty
        variant.save()

        order_item_id = Itemstatus.objects.get(id=6)
        orderitem_id.orderitem_status = order_item_id
        total_p = orderitem_id.price
        print(total_p, '5444444444444444')
        orderitem_id.save()

        try:
            # total item_status
            all_order_item = OrderItem.objects.filter(order=view_id)

            # import pdb
            # pdb.set_trace()
            total_count = all_order_item.count()

            Pending = all_order_item.filter(orderitem_status__id=1).count()
            Processing = all_order_item.filter(orderitem_status__id=2).count()
            Shipped = all_order_item.filter(orderitem_status__id=3).count()
            Delivered = all_order_item.filter(orderitem_status__id=4).count()
            Cancelled = all_order_item.filter(orderitem_status__id=5).count()
            Return = all_order_item.filter(orderitem_status__id=6).count()

            if total_count == Pending:
                total_value = 1
            elif total_count == Processing:
                total_value = 2
            elif total_count == Shipped:
                total_value = 3
            elif total_count == Delivered:
                total_value = 4
            elif total_count == Cancelled:
                total_value = 5
            elif total_count == Return:
                total_value = 6
            else:
                total_value = 1

        except:
            return redirect('order_detail', view_id)

        change_all_items_status = Order.objects.get(id=view_id)
        item_status_instance_all = Orderstatus.objects.get(id=total_value)
        change_all_items_status.order_status = item_status_instance_all
        change_all_items_status.save()

        try:
            wallet = Wallet.objects.get(user=request.user)
            wallet = wallet + total_p
            wallet.save()

        except Wallet.DoesNotExist:
            wallet = Wallet.objects.create(user=request.user, wallet=total_p)

        orderitem_id.save()
        messages.success(request, 'Your Order Returned Successfully')
        return redirect('order_detail', view_id)

    return redirect('userprofile')
