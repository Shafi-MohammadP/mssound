import re
from django.shortcuts import render, redirect
from .models import Coupon
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url='admin_login1')
def coupon(request):
    context = {
        'coupon': Coupon.objects.filter(is_available=True).order_by('id')
    }

    return render(request, 'dashboard/coupon.html', context)


def add_coupon(request):

    if request.method == 'POST':

        coupon_name = request.POST.get('coupon_name')
        coupon_code = request.POST.get('coupon_code')
        minimum_price = request.POST.get('minimum_price')
        coupon_discount_amount = request.POST.get('coupon_discount_amount')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')

        if coupon_name is None or coupon_name.strip() == '':
            messages.error(request, 'Coupon name is Blank')
            return redirect('coupon')
        if not re.search(r'\b[A-Z0-9a-z]{2,}\b', coupon_code):
            messages.error(
                request, " Coupen code must inlcude letters and numbers!")
            return redirect('coupon')
        if minimum_price.strip() == '':
            messages.error(request, 'Minimum Price is Compulsory')
            return redirect('coupon')
        minimum_price = int(minimum_price)
        print(minimum_price, '64555555555555555555')

        if minimum_price <= 0:
            messages.error(request, 'Positive Numbers Only')
            return redirect('coupon')

        if coupon_discount_amount.strip() == '':
            messages.error(request, 'discount Feild Compulsory')
            return redirect('coupon')
        coupon_discount_amount = int(coupon_discount_amount)
        print(coupon_discount_amount, 'dsjffffffffffffffffff')
        if coupon_discount_amount <= 0:
            messages.error(request, 'Positive Numbers Only')
            return redirect('coupon')
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid date format. Use YYYY-MM-DD.")
            return redirect('coupon')

        if start_date >= end_date:
            messages.error(request, 'Starting Date exceede End Date')
            return redirect('coupon')
        if start_date < timezone.now().date():
            messages.error(
                request, 'I know You are samart But dont Be OverSmart')
            return redirect('coupon')

        coupon = Coupon.objects.create(coupon_name=coupon_name, coupon_code=coupon_code, minimum_price=minimum_price,
                                       coupon_discount_amount=coupon_discount_amount, start_date=start_date, end_date=end_date)
        coupon.save()
        messages.success(request, 'Coupon Added Succesfully')
        return redirect('coupon')


def edit_coupon(request, coupon_id):

    if request.method == 'POST':
        coupon_name = request.POST.get('coupon_name')
        coupon_code = request.POST.get('coupon_code')
        minimum_price = request.POST.get('minimum_price')
        coupon_discount_amount = request.POST.get('coupon_discount_amount')
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')

        if coupon_name is None or coupon_name.strip() == '':
            messages.error(request, 'Coupon name is Blank')
            return redirect('coupon')
        if not re.search(r'\b[A-Z0-9a-z]{2,}\b', coupon_code):
            messages.error(
                request, " Coupen code must inlcude letters and numbers!")
            return redirect('coupon')
        if minimum_price.strip() == '':
            messages.error(request, 'Minimum Price is Compulsory')
            return redirect('coupon')
        minimum_price = int(minimum_price)
        print(minimum_price, '64555555555555555555')

        if minimum_price <= 0:
            messages.error(request, 'Positive Numbers Only')
            return redirect('coupon')

        if coupon_discount_amount.strip() == '':
            messages.error(request, 'discount Feild Compulsory')
            return redirect('coupon')
        coupon_discount_amount = int(coupon_discount_amount)
        print(coupon_discount_amount, 'dsjffffffffffffffffff')
        if coupon_discount_amount <= 0:
            messages.error(request, 'Positive Numbers Only')
            return redirect('coupon')
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid date format. Use YYYY-MM-DD.")
            return redirect('coupon')

        if start_date >= end_date:
            messages.error(request, 'Starting Date exceede End Date')
            return redirect('coupon')
        if start_date < timezone.now().date():
            messages.error(
                request, 'Ending date after the strating date')
            return redirect('coupon')

        coupon_edit = Coupon.objects.get(id=coupon_id)
        print(coupon, 'ffffffffffffffffffffffffff')

        coupon_edit.coupon_name = coupon_name
        coupon_edit.coupon_code = coupon_code
        coupon_edit.minimum_price = minimum_price
        coupon_edit.coupon_discount_amount = coupon_discount_amount
        coupon_edit.start_date = start_date
        coupon_edit.end_date = end_date

        coupon_edit.save()
        messages.success(request, 'Coupon Edited Succesfully')
        return redirect('coupon')


def delete_coupon(request, coupon_id):
    try:
        coupon_delete = Coupon.objects.get(id=coupon_id)
        coupon_delete.is_available = False
        coupon_delete.save()
        messages.success(request, "coupon deleted successfully!")
        return redirect('coupon')
    except:
        messages.error(request, "The specified coupon does not exist!")
    return redirect('coupon')
