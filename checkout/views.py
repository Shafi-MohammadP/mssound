from product.models import Product, Color
from variant.models import Variant, VariantImage
# from user.models import CustomUser
from django.http import JsonResponse
from cart.models import Cart
from userprofile.models import Address
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
import random
from wishlist.models import Wishlist
import string
from coupon.models import Coupon
from django.shortcuts import redirect, render
# Create your views here.

# Create your views here.


def checkout(request):
    request.session['coupon_session'] = 0
    request.session['coupon_id'] = None

    if request.method == 'POST':
        coupon = request.POST.get('coupon')
        print(coupon, 'sddddddddddddddddddddddddddddddddddddddddddd')
        if coupon is None:
            messages.error(request, 'coupon field is cannot empty!')
            return redirect('checkout')
        try:
            check_coupons = Coupon.objects.filter(coupon_code=coupon).first()
            cartitems = Cart.objects.filter(user=request.user)
            print(check_coupons, cartitems)
            total_price = 0
            for item in cartitems:
                product_price = item.variant.product.product_price
                total_price += product_price * item.product_qty
                print(check_coupons, cartitems)
            print(check_coupons, cartitems)
            grand_total = total_price
            print(grand_total)
            if grand_total >= check_coupons.minimum_price:
                print(grand_total)
                coupon = check_coupons.coupon_discount_amount
                print(coupon)
                coupon_id = check_coupons.id
                print(coupon_id)

                request.session['coupon_session'] = coupon
                request.session['coupon_id'] = coupon_id
                print(coupon, 'oioooooooooooooooooooooooooooooooooo')
                messages.success(request, 'This coupon added successfully!')
            else:
                coupon = False
                messages.error(request, ' purchase minimum price!')

            address = Address.objects.filter(
                user=request.user, is_available=True)
            cart_count = Cart.objects.filter(user=request.user).count()
            wishlist_count = Wishlist.objects.filter(user=request.user).count()
            coupon_checkout = Coupon.objects.filter(is_available=True)
            print(coupon)

            context = {

                'coupon_checkout': coupon_checkout,
                'cartitems': cartitems,
                'total_price': total_price,
                'grand_total': grand_total,
                'address': address,
                'wishlist_count': wishlist_count,
                'cart_count': cart_count,
                'coupon': coupon

            }
            print(coupon)
            if total_price == 0:
                return redirect('home')
            else:
                return render(request, 'checkout/checkout.html', context)

        except:
            messages.error(request, 'This coupon not valid!')
            return redirect('checkout')

    cartitems = Cart.objects.filter(user=request.user)

    total_price = 0
    for item in cartitems:
        product_price = item.variant.product.product_price
        total_price += product_price * item.product_qty

    grand_total = total_price

    address = Address.objects.filter(user=request.user, is_available=True)
    cart_count = Cart.objects.filter(user=request.user).count()
    wishlist_count = Wishlist.objects.filter(user=request.user).count()
    coupon_checkout = Coupon.objects.filter(is_available=True)
    coupon = False

    context = {
        'coupon_checkout': coupon_checkout,
        'cartitems': cartitems,
        'total_price': total_price,
        'grand_total': grand_total,
        'address': address,
        'wishlist_count': wishlist_count,
        'cart_count': cart_count,
        'coupon': coupon,

    }
    if total_price == 0:
        return redirect('home')
    else:

        return render(request, 'checkout/checkout.html', context)


def placeorder(request):
    if request.method == 'POST':
        # Retrieve the current user

        user = request.user
        # Retrieve the address ID from the form data
        address_id = request.POST.get('address')
        coupon = request.POST.get('couponOrder')
        # print(coupon, '6grrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr')
        # print(address_id, '655655555555555555555555555555555555')
        if address_id is None:
            messages.error(request, 'Address field is mandatory!')
            return redirect('checkout')

        # Retrieve the selected address from the database
        address = Address.objects.get(id=address_id)
        # print(address, '656565656666666666666666666666666666666')

        # Create a new Order instance and set its attributes
        neworder = Order()
        neworder.address = address
        neworder.user = user
        neworder.payment_mode = request.POST.get('payment_method')
        neworder.message = request.POST.get('order_note')
        session_coupon_id = request.session.get('coupon_id')

        if session_coupon_id != None:
            session_coupons = Coupon.objects.get(id=session_coupon_id)
        else:
            session_coupons = None

        neworder.coupon = session_coupons
        # neworder.message = request.POST.get('order_note')

        # Calculate the cart total price
        cart_items = Cart.objects.filter(user=user)
        cart_total_price = 0

        for item in cart_items:
            product_price = item.variant.product.product_price
            cart_total_price += product_price * item.product_qty
        # print(cart_total_price, 'weeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')

        session_coupon = request.session.get('coupon_session')
        # print(session_coupon, 'sfffffffffffffffffffffffffffffffff')
        cart_total_amount = cart_total_price - session_coupon
        neworder.total_price = cart_total_amount

        # print(cart_total_amount, '11111111111111111111111111111111111')

        # Generate a unique tracking number
        track_no = random.randint(1111111, 9999999)
        while Order.objects.filter(tracking_no=track_no).exists():
            track_no = random.randint(1111111, 9999999)
        neworder.tracking_no = track_no
        # print(track_no, '22222222222222222222222222222222222222222222')

        neworder.payment_id = generate_random_payment_id(10)
        while Order.objects.filter(payment_id=neworder.payment_id).exists():
            neworder.payment_id = generate_random_payment_id(10)
        # print(track_no, '22222222222222222222222222222222222222222222')
        # print(neworder.payment_id)
        # print(neworder.tracking_no)
        # print(neworder.address)
        # print(neworder.user)
        # print(neworder.payment_mode)
        # print(neworder.coupon)

        neworder.save()

        # Create OrderItem instances for each cart item
        for item in cart_items:
            OrderItem.objects.create(
                order=neworder,
                variant=item.variant,
                price=item.variant.product.product_price,
                quantity=item.product_qty
            )

            # Decrease the product quantity from the available stock
            product = Variant.objects.filter(id=item.variant.id).first()
            product.quantity -= item.product_qty
            product.save()

        # Delete the cart items after the order is placed
            cart_items.delete()

        payment_mode = request.POST.get('payment_method')
        if payment_mode == 'cod' or payment_mode == 'razorpay':
            del request.session['coupon_session']
            del request.session['coupon_id']

            return JsonResponse({'status': "Your order has been placed successfully"})

    return redirect('checkout')


def generate_random_payment_id(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))


def razarypaycheck(request):
    cart = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cart:
        total_price = total_price + item.variant.product.product_price * item.product_qty
    return JsonResponse({'total_price': total_price})
