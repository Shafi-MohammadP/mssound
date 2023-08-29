from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import Product, Color, ProductReview
from variant.models import Variant, VariantImage
# from categories.models import category

from django.db.models import Sum, Q
from django.db.models.functions import TruncDay
from django.db.models import DateField
from django.db.models.functions import Cast
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# verification email
from user.models import UserOTP
from user.views import validateemail, validatepassword
from django.contrib import auth
from django.core.mail import send_mail
from django.conf import settings
from category.models import category
import random
import re
from django.core.exceptions import ValidationError


# Create your views here.
@login_required(login_url='admin_login1')
def product(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    product = Product.objects.all().order_by('id')

    product_list = {
        'product': product,
        # 'variant'  : variant,
        'categories': category.objects.all(),


    }
    return render(request, 'product/products.html', product_list)


@login_required(login_url='admin_login1')
def addproduct(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    if request.method == 'POST':
        name = request.POST['product_name']
        price = request.POST['product_price']
        category_id = request.POST.get('category')
        product_description = request.POST.get('product_description')
        # Validation
        if Product.objects.filter(product_name=name).exists():
            messages.error(request, 'Product name already exists')
            return redirect('product')

        if name.strip() == '' or price.strip() == '':
            messages.error(request, "Name or Price field are empty!")
            return redirect('product')

        category_obj = category.objects.get(id=category_id)

        # Save
        product = Product(

            product_name=name,
            category=category_obj,
            product_price=price,
            slug=name,
            product_description=product_description,

        )
        product.save()
        messages.success(request, 'product added successfully!')
        return redirect('product')

    return render(request, 'products/products.html')


def product_delete(request, product_id):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    delete_product = Product.objects.get(id=product_id)
    variants = Variant.objects.filter(product=delete_product)
    print(variants)
    for variant in variants:
        variant.is_available = False
        variant.quantity
        variant.save()

    delete_product.is_available = False
    delete_product.save()
    messages.success(request, 'product deleted successfully!')
    return redirect('product')


def product_edit(request, product_id):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    if request.method == 'POST':
        name = request.POST['product_name']
        price = request.POST['product_price']
        category_id = request.POST.get('category')
        product_description = request.POST.get('product_description')

        if name.strip() == '' or price.strip() == '':
            messages.error(request, "Name or Price field are empty!")
            return redirect('product')

        category_obj = category.objects.get(id=category_id)

        if Product.objects.filter(product_name=name).exists():

            check = Product.objects.get(id=product_id)

            if name == check.product_name:
                pass
            else:
                messages.error(request, 'Product name already exists')
                return redirect('product')

        editproduct = Product.objects.get(id=product_id)
        editproduct.product_name = name
        editproduct.product_price = price
        editproduct.category = category_obj
        editproduct.product_description = product_description
        editproduct.save()
        messages.success(request, 'product edited successfully!')

        return redirect('product')


def product_view(request, product_id):
    if not request.user.is_superuser:
        return redirect('admin_login1')

    variant = Variant.objects.filter(product=product_id)
    color_name = Color.objects.all().order_by('id')
    product = Product.objects.all().order_by('id')
    variant_list = {
        'variant': variant,
        'color_name': color_name,
        'product': product,
    }
    return render(request, 'View/product_view.html', variant_list)


def add_review(request):

    if request.method == 'POST':
        if request.user.is_authenticated:
            rating = int(request.POST.get('rating'))
            review_text = request.POST.get('review')
            name = request.POST.get('name')
            email = request.POST.get('email')
            product_id = request.POST.get('product_id')
            img_id = request.POST.get('img_id')

            print(rating, review_text, name, email, product_id, '111111111111')

            # Get the product instance based on the product_id
            product = Product.objects.get(id=product_id)

            if rating == 0:
                messages.error(request, 'Please Select Stars!')
                return redirect('product_show', product_id, img_id)

            if request.user.email == email:
                # Create and save the product review associated with the product
                review = ProductReview.objects.create(
                    product=product,
                    rating=rating,
                    review_text=review_text,
                    name=name,
                    email=email
                )

                messages.success(request, 'Review added successfully!')
                return redirect('product_show', product_id, img_id)

            else:
                messages.error(
                    request, 'Invalid email! Please log in with the correct email!')
                return redirect('product_show', product_id, img_id)

        else:
            messages.error(request, 'Login to continue!')
            return redirect('product_show', product_id, img_id)

    messages.error(request, 'Invalid request method!')

    return redirect('product_show', product_id, img_id)


def Product_Search(request):
    if request.method == 'POST':

        serach = request.POST.get('search')
        print(serach, 'hfduisuifgbuybghafddddddddddddddddddddddddddddddddddddddddddddddddddguy')
        if serach is None or serach.strip() == '':
            messages.error(request, 'Field Cannot Empty')
            return redirect('product')

        product = Product.objects.filter(
            Q(product_name__icontains=serach))

    if product:
        pass
    else:
        messages.error(request, 'Item Not Founnd')
        return redirect('product')

    categories = category.objects.all()

    return render(request, 'product/products.html', {'product': product, 'categories': categories})


# @login_required(login_url='admin_login1')
# def addproduct(request):
#     if request.method=='POST':
#         name = request.POST['product_name']
#         price = request.POST['product_price']
#         image = request.FILES.get('product_image', None)
#         color = request.POST.get('product_color')
#         quantity = request.POST.get('product_quantity')


#         if Product.objects.filter(product_name=name).exists():
#             messages.error(request, 'Product name already exist')
#             return redirect('product')
#         if name =='' or price =='':
#             messages.error(request, 'Name or price feilds are empty')
#             return redirect('product')
#         if not image:
#             messages.error(request, 'image not uploaded')
#             return redirect('product')


#         prodect = Product(
#              product_name = name,
#              product_price = price,
#              product_image = image,
#              product_color = color,
#              product_quantity = quantity,
#          )
#         prodect.save()
#         return redirect('product')
#     return render(request, 'product/product.html')


# @login_required(login_url='admin_login1')
# def editproduct(request, editproduct_id):

#     # try:
#     #     prodect = Product.objects.get(slug=editproduct_id)
#     # except Product.DoesNotExist:
#     #     messages.error(request, 'product not found')
#     if request.method=='POST':
#         prname = request.POST['product_name']
#         prprice = request.POST['product_price']
#         prcolor = request.POST['product_color']
#         prquantity = request.POST.get('product_quantity')


#         try:
#             prod = Product.objects.get(slug=editproduct_id)
#             image = request.FILES.get('product_image')
#             if image:
#                 prod.product_image= image
#                 prod.save()
#         except Product.DoesNotExist:
#             messages.error(request, 'image not found')
#             return redirect('product')

#         if prname == '' or prprice == '':
#             messages.error(request, 'Name or Price field is empty')
#             return redirect('product')
#         if Product.objects.filter(product_name=prname).exists():
#             check = Product.objects.get(slug=editproduct_id)
#             if prname != check.product_name:
#                 messages.error(request, 'Product name already exists')
#                 return redirect('product')


#         edited = Product.objects.get(slug=editproduct_id)
#         edited.product_name = prname
#         edited.product_price = prprice
#         edited.product_color = prcolor
#         edited.product_quantity = prquantity
#         edited.save()

#         return redirect('product')
#     else:
#         prodec=Product.objects.all()
#         return render(request, 'product.product.html', {'prodec':prodec})


# @login_required(login_url='admin_login1')
# def deleteproduct(request,deleteproduct_id):
#     pro = Product.objects.get(slug=deleteproduct_id)
#     pro.delete()
#     return redirect('product')
# def productedit(request):

#     return render(request, 'product/createproduct.html')


# @login_required(login_url='admin_login')
# def createproduct(request):
#     if not request.user.is_superuser:
#         return redirect('admin_login')
#     if request.method=='POST':
#         name = request.POST['product_name']
#         price = request.POST['product_price']
#         image = request.FILES.get('product_image', None)
#         description = request.POST['product_description']
#         detailed_description = request.POST['product_description_detailed']

#         if products.objects.filter(product_name=name).exists():
#             messages.error(request, 'Product name already exist')
#             return redirect('product')
#         if name =='' or price =='':
#             messages.error(request, 'Name or price feilds are empty')
#             return redirect('product')
#         if not image:
#             messages.error(request, 'image not uploaded')
#             return redirect('product')

#         #######
#         #########
#         #######
#         prodect = products(
#             product_name = name,
#             product_price = price,
#             product_image = image,
#             product_description = description,
#             product_description_detailed = detailed_description,
#         )
#         prodect.save()
#         return redirect('product')
#     return render(request, 'product/product.html')
