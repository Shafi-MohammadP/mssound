from django.shortcuts import render
from django.db.models import Sum, Avg
from django.shortcuts import render
from category.models import category
from variant.models import VariantImage, Variant
from product.models import Product, Color, ProductReview
from cart.models import Cart
from wishlist.models import Wishlist
from django.db.models import Q
from decimal import Decimal

# Create your views here.


def Shop_Filtering(request):

    if request.method == 'POST':
        color = request.POST.get('colorfilter')
        categories = request.POST.get('categoryfilter')
        pricefilter = request.POST.get('pricefilter')
        print(pricefilter, '-------------------------------------------------------------------')

        if categories and color:
            variant_images = (VariantImage.objects.filter(variant__color__id=color, variant__product__category__id=categories,
                              variant__product__is_available=True).order_by('variant__product').distinct('variant__product'))

        elif color:
            variant_images = (VariantImage.objects.filter(variant__color__id=color, variant__product__is_available=True).order_by(
                'variant__product').distinct('variant__product'))
        elif categories:
            variant_images = (VariantImage.objects.filter(
                variant__product__category__id=categories, variant__product__is_available=True).order_by('variant__product').distinct('variant__product'))

        elif pricefilter:

            price_min, price_max = map(Decimal, pricefilter.split('-'))
            variant_images = VariantImage.objects.filter(
                Q(variant__product__product_price__gte=price_min) &
                Q(variant__product__product_price__lt=price_max) &
                Q(variant__product__is_available=True)
            ).order_by('variant__product').distinct('variant__product')
            print(pricefilter, 'dddddddddddddddddddddddddddddddddddddddddddddddddd')

        else:
            variant_images = (VariantImage.objects.filter(variant__product__is_available=True).order_by(
                'variant__product').distinct('variant__product'))

    reviews = ProductReview.objects.all()
    ratings = Product.objects.annotate(avg_rating=Avg('reviews__rating'))
    categories = category.objects.all()
    colors = Color.objects.all()
    try:
        cart_count = Cart.objects.filter(user=request.user).count()
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    except:
        cart_count = False
        wishlist_count = False

    context = {
        'categories': categories,
        'variant_images': variant_images,
        'cart_count': cart_count,
        'wishlist_count': wishlist_count,
        'reviews': reviews,
        'ratings': ratings,
        'colors': colors,
        'pricefilter': pricefilter
    }

    return render(request, 'shop/shop.html', context)
