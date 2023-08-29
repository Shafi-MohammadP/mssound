# from .models import Product, VariantImage, category
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control, never_cache

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from product.models import Color, Product, ProductReview
from variant.models import Variant, VariantImage
from category.models import category
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth.password_validation import validate_password
from django.db.models import Sum, Avg, Count,  Q, Subquery, OuterRef
# from .models import UserOTP
import re
import random
from django.conf import settings
import random
from cart.models import Cart
from django.core.mail import send_mail
from django.core.validators import validate_email
from wishlist.models import Wishlist
from checkout.models import Order
from datetime import datetime, timedelta
from django.contrib import messages, auth
from .models import Contacts
# Create your views here.


def home(request):
    categories = category.objects.all()
    products = Product.objects.all()
    variant_images = VariantImage.objects.order_by(
        'variant__product').distinct('variant__product')
    variant_imagess = VariantImage.objects.order_by(
        'variant__product__product_price').distinct('variant__product__product_price')
    print(variant_imagess,
          '------------------------------------------------------------------------')
    variant_imaagess = VariantImage.objects.filter(
        variant__color__color_name='black').distinct()
    inEar = VariantImage.objects.filter(
        variant__product__category__categories='In-Ear Wireles').distinct('variant__product')
    Neckband = VariantImage.objects.filter(
        variant__product__category__categories='Neckband').distinct('variant__product')
    OverEar = VariantImage.objects.filter(
        variant__product__category__categories='Over-ear headphones').distinct('variant__product')
    InEar_Wired = VariantImage.objects.filter(
        variant__product__category__categories='In-Ear Wired').distinct('variant__product')
    print(InEar_Wired)

    reviews = ProductReview.objects.all()
    ratings = Product.objects.annotate(avg_rating=Avg('reviews__rating'))
    try:
        cart_count = Cart.objects.filter(user=request.user).count()
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    except:
        cart_count = False
        wishlist_count = False

    context = {
        'categories': categories,
        'products': products,
        'variant_images': variant_images,
        'variant_imagess': variant_imagess,
        'variant_imaagess': variant_imaagess,
        'reviews': reviews,
        'ratings': ratings,
        'cart_count': cart_count,
        'wishlist_count': wishlist_count,
        'inEar': inEar,
        'InEar_Wired': InEar_Wired,
        'OverEar': OverEar,
        'Neckband': Neckband

    }
    print(wishlist_count, '6545654adssssssFfffffffffffffffffs')
    print(cart_count, '6545654adssssssFfffffffffffffffffs')

    return render(request, 'home.html', context)


# def product_show(request, prod_id, img_id):

#     variant = VariantImage.objects.filter(variant=img_id)
#     variant_images = VariantImage.objects.filter(
#         variant__product__id=prod_id).distinct('variant__product')
#     color = VariantImage.objects.filter(
#         variant__product__id=prod_id).distinct('variant__color')
#     context = {
#         'variant': variant,
#         'color': color,
#         'variant_images': variant_images,
#         # 'cart':cart
#     }

#     return render(request, 'product/product_show.html', context)
def product_show(request, prod_id, img_id):

    variant = VariantImage.objects.filter(variant=img_id, is_available=True)
    variant_images = VariantImage.objects.filter(
        variant__product__id=prod_id, is_available=True).distinct('variant__product')
    # size =VariantImage.objects.filter(variant__product__id=prod_id).distinct('variant__size')
    color = VariantImage.objects.filter(
        variant__product__id=prod_id, is_available=True).distinct('variant__color')
    reviews = ProductReview.objects.filter(product=prod_id)
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    rev_count = ProductReview.objects.filter(product=prod_id).count()

    try:
        cart_count = Cart.objects.filter(user=request.user).count()
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    except:
        cart_count = False
        wishlist_count = False
    try:
        average_rating = int(average_rating)
    except:
        average_rating = 0
    context = {
        'variant': variant,
        'color': color,
        'variant_images': variant_images,
        'reviews': reviews,
        'average_rating': average_rating,
        'rev_count': rev_count,
        'wishlist_count': wishlist_count,
        'cart_count': cart_count,
    }

    return render(request, 'product/product_show.html', context)


def shop(request):
    categories = category.objects.all()
    variant_images = VariantImage.objects.order_by(
        'variant__product').distinct('variant__product')
    variant_images = VariantImage.objects.filter(variant__product__is_available=True).order_by(
        'variant__product').distinct('variant__product')

    colors = Color.objects.all()
    try:
        cart_count = Cart.objects.filter(user=request.user).count()
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    except:
        cart_count = False
        wishlist_count = False

    reviews = ProductReview.objects.all()
    ratings = Product.objects.annotate(avg_rating=Avg('reviews__rating'))

    context = {
        'categories': categories,
        'variant_images': variant_images,
        'cart_count': cart_count,
        'wishlist_count': wishlist_count,
        'reviews': reviews,
        'ratings': ratings,
        'colors': colors
    }

    return render(request, 'shop/shop.html', context)


def search_view(request):
    search_query = request.POST.get('search')
    print("------------------", search_query)
    variant_images = VariantImage.objects.filter(
        variant__product__product_name__icontains=search_query, is_available=True).distinct('variant__product__product_name')
    # ratings = Product.objects.annotate(avg_rating=Avg('reviews__rating'))
    try:
        cart_count = Cart.objects.filter(user=request.user).count()
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    except:
        cart_count = False
        wishlist_count = False

    return render(request, 'shop/shop.html', {'variant_images': variant_images, 'wishlist_count': wishlist_count, 'cart_count': cart_count, })


def QuickView(request, product_id, image_id):

    variant = VariantImage.objects.filter(variant=image_id, is_available=True)
    variant_images = VariantImage.objects.filter(
        variant__product__id=product_id, is_available=True).distinct('variant__product')
    # size =VariantImage.objects.filter(variant__product__id=prod_id).distinct('variant__size')
    color = VariantImage.objects.filter(
        variant__product__id=product_id, is_available=True).distinct('variant__color')
    reviews = ProductReview.objects.filter(product=product_id)
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    rev_count = ProductReview.objects.filter(product=product_id).count()
    try:
        average_rating = int(average_rating)
    except:
        average_rating = 0
    context = {
        'variant': variant,
        'color': color,
        'variant_images': variant_images,
        'reviews': reviews,
        'average_rating': average_rating,
        'rev_count': rev_count,

    }

    return render(request, 'popup/quickview.html', context)


def product_list(request):
    search_query = request.POST.getlist('search')
    print("------------------", search_query)
    variant_images = VariantImage.objects.filter(
        variant__product__category__categories_in=search_query).distinct('variant__product__product_name')

    return render(request, 'filter/filter.html', variant_images)


@login_required(login_url='user_login1')
def track_order(request):
    last_order = Order.objects.filter(user=request.user).last()
    date = last_order.created_at+timedelta(days=4)

    context = {
        'last_order': last_order,
        'date': date
    }
    return render(request, 'TrackOrder/trackorder.html', context)


def Contact_Us(request):

    return render(request, 'Contact/contact.html')


def Contact_User(request):
    if request.method == 'POST':

        name = request.POST['name']
        email = request.POST['email']
        phonenumber = request.POST['phonenumber']
        subject = request.POST['subject']
        message = request.POST['message']
        if (name.strip() == '' or email.strip() == '' or phonenumber.strip() == ''
                or subject.strip() == '' or message.strip() == ''):
            messages.error(request, 'field cannot empty!')
            return render(request, 'Contact/contact.html')
        email_check = validateemail(email)
        if email_check is False:
            messages.error(request, 'email not valid!')
            return render(request, 'Contact/contact.html')
        if not re.search(re.compile(r'(\+91)?(-)?\s*?(91)?\s*?(\d{3})-?\s*?(\d{3})-?\s*?(\d{4})'), phonenumber):
            messages.error(request, 'phonenumber should only contain numeric!')
            return render(request, 'Contact/contact.html')
        phonenumber_checking = len(phonenumber)
        if not phonenumber_checking == 10:
            messages.error(
                request, 'phonenumber should be must contain 10digits!')
            return render(request, 'Contact/contact.html')
        contact = Contacts.objects.create(
            name=name, phone_number=phonenumber, email=email, subject=subject, message=message)
        contact.save()
        messages.success(request, 'your contact has been submited!')
        return render(request, 'Contact/contact.html')


def validateemail(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def validatepassword(new_password):
    try:
        validate_password(new_password)
        return True
    except ValidationError:
        return False
