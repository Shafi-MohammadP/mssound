import csv
import io
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
# from categories.models import category
from django.db.models import Sum
from django.db.models.functions import TruncDay
from django.db.models import DateField
from django.db.models.functions import Cast
from datetime import date, datetime, timedelta
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from checkout.models import OrderItem, Order
# from home.models import Contacts

# verification email
from user.models import UserOTP
from user.views import validateemail, validatepassword
from django.contrib import auth
from django.core.mail import send_mail
from django.conf import settings
import random
import re
from django.core.exceptions import ValidationError
from itertools import groupby
from category.models import category as Category
from django.db.models.functions import TruncMonth
from fpdf import FPDF
from django.http import HttpResponse
from datetime import datetime
from django.db.models import Prefetch


def admin_signup(request):

    if request.method == 'POST':

        get_otp = request.POST.get('otp')
        if get_otp:
            get_email = request.POST.get('email')
            user = User.objects.get(email=get_email)

            if int(get_otp) == UserOTP.objects.filter(user=user).last().otp:
                user.is_active = True
                user.save()
                auth.login(request, user)
                # messages.success(request,f'Account is created for {user.email}')
                UserOTP.objects.filter(user=user).delete()
                return redirect('usermanagement_1')
            else:
                messages.warning(request, f'you Entered a Wrong OTP')
                return render(request, 'dashboard/admin_signup.html', {'otp': True, 'user': user})
        else:
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']

            context = {
                'pre_username': username,
                'pre_email': email,
                'pre_password1': password1,
            }

            if username.strip() == '' or password1.strip() == '' or email.strip() == '':
                messages.error(request, 'field cannot empty!')
                return render(request, 'dashboard/admin_signup.html', context)

            elif User.objects.filter(username=username):
                messages.error(request, 'username alredy exist!')
                context['pre_username'] = ''
                return render(request, 'dashboard/admin_signup.html', context)

            elif not re.match(r'^[a-zA-Z\s]*$', username):
                messages.error(
                    request, 'Username should only contain alphabets!')
                context['pre_username'] = ''
                return render(request, 'dashboard/admin_signup.html', context)

            elif User.objects.filter(email=email):
                messages.error(request, 'email already exist!')
                context['pre_email'] = ''
                return render(request, 'dashboard/admin_signup.html', context)

            email_check = validateemail(email)
            if email_check is False:
                messages.error(request, 'email not valid!')
                context['pre_email'] = ''
                return render(request, 'dashboard/admin_signup.html', context)

            password_check = validatepassword(password1)
            if password_check is False:
                messages.error(request, 'Enter strong password!')
                context['pre_password1'] = ''
                return render(request, 'dashboard/admin_signup.html', context)

            user = User.objects.create_user(
                username=username, email=email, password=password1)
            user.is_active = False
            user.is_superuser = True
            user.is_staff = True
            user.save()
            user_otp = random.randint(100000, 999999)
            UserOTP.objects.create(user=user, otp=user_otp)
            mess = f'Hello \t{user.username},\nYour OTP to verify your account for MS Sounds is {user_otp}\n Thanks You!'
            send_mail(
                "Welcome to MS Sounds , verify your Email",
                mess,
                settings.EMAIL_HOST_USER,
                [user.email],

                fail_silently=False
            )
            return render(request, 'dashboard/admin_signup.html', {'otp': True, 'user': user})

    return render(request, 'dashboard/admin_signup.html')


def usermanagement_1(request):

    return render(request, 'dashboard/dashboardbase.html')

    # return render(request,'dashboard/usermanagement.html')


def admin_login1(request):
    # if request.user.is_authenticated:
    #     return redirect('home')#dashboard user

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if username.strip() == '' or password.strip() == '':
            messages.error(request, 'field cannot empty!')
            return redirect('admin_login1')

        user = authenticate(username=username, password=password)

        if user is not None:

            if user.is_active:
                if user.is_superuser:
                    login(request, user)
                    return redirect('dashboardog')  # dashboard user
                else:
                    messages.warning(request, 'your not admin!')
                return redirect('admin_login1')

            else:
                messages.warning(request, 'your account has been blocked!')
                return redirect('admin_login1')

        else:
            messages.error(request, 'invalid username or password!')
            return redirect('admin_login1')

    return render(request, 'dashboard/admin_login1.html')


@login_required(login_url='admin_login1')
def dashboard(request):
    return render(request, 'dashboard/dashboardbase.html')


@login_required(login_url='admin_login1')
def dashboardog(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')

    sales_data = OrderItem.objects.values('order__created_at__date').annotate(
        total_sales=Sum('price')).order_by('-order__created_at__date')
    # Prepare data for the chart
    categories = [item['order__created_at__date'].strftime(
        '%d/%m') for item in sales_data]
    sales_values = [item['total_sales'] for item in sales_data]

    return_data = OrderItem.objects.filter(orderitem_status__item_status__in=["Return", "Cancelled"]).values(
        'order__created_at__date').annotate(total_returns=Sum('price')).order_by('-order__created_at__date')
    return_values = [item['total_returns'] for item in return_data]
    orders = Order.objects.order_by('-created_at')[:10]
    context = {
        'orders': orders,
        'categories': categories,
        'sales_values': sales_values,
        'return_values': return_values,
    }
    return render(request, 'dashboard/dash.html', context)


def admin_forgotpassword(request):
    if request.method == 'POST':
        get_email = request.POST.get('email')
        user = User.objects.filter(email=get_email).first()
        if not user:
            messages.error(request, 'email does not exist!')
            return render(request, 'dashboard/password_admin_forgot.html')
        if user.is_superuser:
            get_otp = request.POST.get('otp')
            if get_otp:
                get_email = request.POST.get('email')
                user = User.objects.get(email=get_email)
                if int(get_otp) == UserOTP.objects.filter(user=user).last().otp:
                    password1 = request.POST.get('password1')
                    password2 = request.POST.get('password2')
                    context = {
                        'pre_otp': get_otp,
                    }
                    if password1.strip() == '' or password2.strip() == '':
                        messages.error(request, 'field cannot empty !')
                        return render(request, 'dashboard/password_admin_forgot.html', {'otp': True, 'user': user, 'pre_otp': get_otp})

                    elif password1 != password2:
                        messages.error(request, 'Password does not match!')
                        return render(request, 'dashboard/password_admin_forgot.html', {'otp': True, 'user': user, 'pre_otp': get_otp})

                    Pass = validatepassword(password1)
                    if Pass is False:
                        messages.error(
                            request, 'Please enter Strong password!')
                        return render(request, 'dashboard/password_admin_forgot.html', {'otp': True, 'user': user, 'pre_otp': get_otp})
                    user.set_password(password1)
                    user.save()
                    UserOTP.objects.filter(user=user).delete()
                    messages.success(request, 'Your password is changed!')
                    return redirect('admin_login1')
                else:
                    messages.warning(request, 'You Entered a wrong OTP!')
                    return render(request, 'dashboard/password_admin_forgot.html', {'otp': True, 'user': user})
            else:
                email = request.POST['email']

                if email.strip() == '':
                    messages.error(request, 'field cannot empty!')
                    return render(request, 'dashboard/password_admin_forgot.html')

                email_check = validateemail(email)
                if email_check is False:
                    messages.error(request, 'email not valid!')
                    return render(request, 'dashboard/password_admin_forgot.html')

                if User.objects.filter(email=email):
                    user = User.objects.get(email=email)
                    user_otp = random.randint(100000, 999999)
                    UserOTP.objects.create(user=user, otp=user_otp)
                    message = f'Hello\t{user.username},\n Your OTP to verify your account for MS Sounds is {user_otp}\n Thanks'
                    send_mail(
                        "welcome to MS Sounds Verify Email",
                        message,
                        settings.EMAIL_HOST_USER,
                        [user.email],
                        fail_silently=False
                    )
                    return render(request, 'dashboard/password_admin_forgot.html', {'otp': True, 'user': user})
                else:
                    messages.error(request, 'email does not exist!')
                    return render(request, 'dashboard/password_admin_forgot.html')
        else:
            messages.error(request, 'you are not admin!')
            return render(request, 'dashboard/password_admin_forgot.html')

    return render(request, 'dashboard/password_admin_forgot.html')


@login_required(login_url='admin_login1')
def admin_logout1(request):
    logout(request)
    return redirect('admin_login1')


@login_required(login_url='admin_login1')
def users_listing(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    user_data = User.objects.all().order_by('id')
    return render(request, 'dashboard/usermanagement.html', {'users': user_data})


@login_required(login_url='admin_login1')
def blockuser(request, user_id):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    user = User.objects.get(id=user_id)
    if user.is_active:
        user.is_active = False
        user.save()
    else:
        user.is_active = True
        user.save()
    return redirect('users_listing')


@login_required(login_url='admin_login1')
def sales_report(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')

    if request.method == 'GET':
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

            if start_date > end_date:
                messages.error(request, 'Start date must be before end date')
                return redirect('sales_report')

            if end_date > date.today():
                messages.error(request, 'End date exceeded to future')
                return redirect('sales_report')
            orders = Order.objects.filter(
                created_at__date__range=(start_date, end_date))
            recent_orders = orders.order_by('-created_at')
        else:
            recent_orders = Order.objects.order_by('-created_at')[:10]
            orders = Order.objects.all()

    total_sales = sum(order.total_price for order in orders)
    total_orders = orders.count()

    sales_by_status = {
        'Pending': orders.filter(order_status=1).count(),
        'Processing': orders.filter(order_status=2).count(),
        'Shipped': orders.filter(order_status=3).count(),
        'Delivered': orders.filter(order_status=4).count(),
        'Cancelled': orders.filter(order_status=5).count(),
        'Return': orders.filter(order_status=6).count(),
    }

    sales_report = {
        'start_date': start_date.strftime('%Y-%m-%d') if start_date else '',
        'end_date': end_date.strftime('%Y-%m-%d') if end_date else '',
        'total_sales': total_sales,
        'total_orders': total_orders,
        'sales_by_status': sales_by_status,
        'recent_orders': recent_orders,
    }

    return render(request, 'dashboard/sales_report.html', {'sales_report': sales_report})


@login_required(login_url='admin_login1')
def Dowload_CSV(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + \
        str(datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['user', 'total_price', 'payment_method', 'tracking_no',
                    'Oredered at', 'product_name', 'product_price', 'product_quantity'])

    orders = Order.objects.all()

    for order in orders:
        order_items = OrderItem.objects.filter(
            order=order).select_related('variant')
        grouped_order_items = groupby(order_items, key=lambda x: x.order_id)
        for order_id, items_group in grouped_order_items:
            items_list = list(items_group)
            for order_item in items_list:
                writer.writerow([
                    order.user.first_name if order_item == items_list[0] else "",
                    order.total_price if order_item == items_list[0] else "",
                    order.payment_mode if order_item == items_list[0] else "",
                    order.tracking_no if order_item == items_list[0] else "",
                    order.created_at if order_item == items_list[0] else "",
                    order_item.variant.product.product_name,
                    order_item.price,
                    order_item.quantity,
                ])
    return response


@login_required(login_url='admin_login1')
def generate_pdf(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + \
        str(datetime.now()) + '.pdf'
    w_pt = 12 * 40  # 8.5 inches width
    h_pt = 11 * 20   # 11 inches height

    pdf = FPDF(format=(w_pt, h_pt))
    pdf.add_page()
    # Enable auto page break with 15mm margin
    pdf.set_auto_page_break(auto=True, margin=15)

    # Set font styles
    pdf.set_font('Arial', 'B', 12)  # Reduce font size for better readability

    # Header Information
    pdf.cell(0, 10, 'Order Details Report', 0, 1, 'C')
    pdf.cell(0, 10, str(datetime.now()), 0, 1, 'C')
    # Table Data
    data = [['User', 'Total Price', 'Payment Mode', 'Tracking No',
             'Ordered At', 'Product Name', 'Product Price', 'Product Quantity']]
    orders = Order.objects.all().prefetch_related(
        Prefetch('orderitem_set',
                 queryset=OrderItem.objects.select_related('variant'))
    )
    for order in orders:
        order_items = order.orderitem_set.all()
        for index, order_item in enumerate(order_items):
            data.append([
                order.user.first_name if index == 0 else "",
                order.total_price if index == 0 else "",
                order.payment_mode if index == 0 else "",
                order.tracking_no if index == 0 else "",
                str(order.created_at.date()) if index == 0 else "",
                order_item.variant.product.product_name,
                order_item.price,
                order_item.quantity,
            ])
    # Create Table
    col_width = 60
    row_height = 10
    for row in data:
        for item in row:
            pdf.cell(col_width, row_height, str(item), border=1)
        pdf.ln()
    response.write(pdf.output(dest='S').encode('latin1'))
    return response


def search_user(request):
    search = request.POST.get('search')
    if search is None or search.strip() == '':
        messages.error(request, 'Fields Cannot empty')
        return redirect('users_listing')

    users = User.objects.filter(
        Q(first_name__icontains=search) | Q(email__icontains=search))
    if users:
        pass
    else:
        users: False
        messages.error(request, 'Search Not Found')
        return redirect('users_listing')

    return render(request, 'dashboard/usermanagement.html', {'users': users})


def user_status_search(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name == 'Active':
            users = User.objects.filter(is_active=True)
            print('dsaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
            print(users)
            return render(request, 'dashboard/usermanagement.html', {'users': users})
        if name == 'Blocked':
            users = User.objects.filter(is_active=False)
            return render(request, 'dashboard/usermanagement.html', {'users': users})
        if name == 'All':
            users = User.objects.all()
            return render(request, 'dashboard/usermanagement.html', {'users': users})
        else:
            return redirect('users_listing')
