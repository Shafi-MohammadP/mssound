from django.shortcuts import redirect, render, get_object_or_404
from product.models import Product, Color
from django.http import Http404
from variant.models import Variant, VariantImage
# from user.models import CustomUser
from django.http import JsonResponse
from cart.models import Cart
from .models import Wishlist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from category.models import category
# Create your views here.


def wishlist(request):
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user).order_by('id')
        variants = wishlist.values_list('variant', flat=True)
        img = VariantImage.objects.filter(
            variant__in=variants).distinct('variant')

        variant_quantity = Variant.objects.filter(
            id__in=variants).values('id', 'quantity')
        quantity_dict = {variant['id']: variant['quantity']
                         for variant in variant_quantity}
        cate = category.objects.all()
        try:
            wishlist_count = Wishlist.objects.filter(user=request.user).count()
            cart_count = Cart.objects.filter(user=request.user).count()
        except:
            wishlist_count = False
            cart_count = False

        context = {
            'wishlist': wishlist,
            'img': img,
            'quantity_dict': quantity_dict,
            'cate': cate,
            'wishlist_count': wishlist_count,
            'cart_count': cart_count,
        }
        return render(request, 'wishlist/wishlist.html', context)
    else:
        return render(request, 'wishlist/wishlist.html')


def add_wishlist(request):

    if request.method == 'POST':
        if request.user.is_authenticated:
            variant_id = request.POST.get('variant_id')
            print(variant_id, '65555555555555555555555555555555555')

            if Wishlist.objects.filter(user=request.user, variant_id=variant_id).exists():

                return JsonResponse({'status': 'Product already in wishlist'})
            else:
                var = Variant.objects.get(id=variant_id)
                Wishlist.objects.create(user=request.user, variant=var)

                return JsonResponse({'status': 'Product added successfully'})
        else:
            return JsonResponse({'status': 'you are not login please login to continue'})

    return redirect('home')


def add_wish_list(request):
    if request.method == 'POST':
        if request.user.is_authenticated:

            variant_id = request.POST.get('variant_id')
            # try:
            #     variant_check =Variant.objects.get(id=variant_id )
            #     if variant_check.size==add_size:
            #         pass
            #     else:
            #         product=variant_check.product
            #         color= variant_check.color
            #         try:
            #             check_variant=Variant.objects.get(product=product, color=color, size=add_size)
            #             variant_id= check_variant.id
            #         except Variant.DoesNotExist:
            #             return JsonResponse({'status': 'Sorry! this variant not available'})

            # except Variant.DoesNotExist:
            #     return JsonResponse({'status': 'No such prodcut found'})

            if Wishlist.objects.filter(user=request.user, variant_id=variant_id).exists():

                return JsonResponse({'status': 'Product already in Wishlist'})

            else:
                Wishlist.objects.create(
                    user=request.user, variant_id=variant_id)
                return JsonResponse({'status': 'Product added successfully in Wishlist'})
        else:
            return JsonResponse({'status': 'you are not login please Login to continue'})

    return redirect('home')


def wish_remove(request, remove_id):
    try:
        wishlist_remove = Wishlist.objects.get(id=remove_id)

        wishlist_remove.delete()
        messages.success(request, 'Items removed succesfully')
    except:
        return redirect('wishlist')

    return redirect('wishlist')

# def add_wishlist(request):
#     if request.method =='POST':
#         if request.user.is_authenticated:

#             variant_id = request.POST.get('variant_id')
#             print(variant_id, '65555555555656665555555555555')


#             if Cart.objects.filter(user=request.user, variant_id=variant_id).exists():

#                 return JsonResponse({'status': 'Product already in cart'})


#             else:
#                 return JsonResponse({'status': 'Product added successfully'})

#         else:
#             return JsonResponse({'status': 'you are not login please Login to continue'})


#     return redirect('home')

# def wish_product_show(request, prod_id, img_id):

#     variant = VariantImage.objects.filter(variant=img_id)
#     variant_images = VariantImage.objects.filter(
#         variant__product__id=prod_id).distinct('variant__product')
#     color = VariantImage.objects.filter(
#         variant__product__id=prod_id).distinct('variant__color')

#     try:
#         product_category = get_object_or_404(category, id=prod_id)
#     except category.DoesNotExist:
#         raise Http404("Category does not exist")
#     context = {
#         'variant': variant,
#         'color': color,
#         'variant_images': variant_images,
#         'product_category': product_category
#         # 'cart':cart
#     }

#     return render(request, 'product/wishproductview.html', context)
