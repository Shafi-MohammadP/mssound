from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control, never_cache

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.contrib.auth.password_validation import validate_password
# from .models import UserOTP
import re
import random
from django.conf import settings
import random
from django.core.mail import send_mail
from django.core.validators import validate_email
from .models import UserOTP

# Create your views here.


def user_login1(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username.strip() == '' or password.strip() == '':
            messages.error(request, "usernmae or pasword is empty")
            return redirect('user_login1')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')
            else:
                messages.warning(request, 'your account has been blocked')
                return redirect('user_login1')
        else:
            messages.error(request, 'invalid username or passworld')
    return render(request, 'user/login.html')


@login_required(login_url='user_login1')
def logout1(request):
    logout(request)
    return redirect('user_login1')


def user_signup(request):
    if request.method == 'POST':
        get_otp = request.POST.get('otp')

        if get_otp:
            get_email = request.POST.get('email')
            usr = User.objects.get(email=get_email)

            if int(get_otp) == UserOTP.objects.filter(user=usr).last().otp:
                usr.is_active = True
                usr.save()
                auth.login(request, usr)
                # messages.success(request,f'Account is created for {usr.email}')
                UserOTP.objects.filter(user=usr).delete()
                return redirect('home')
            else:
                messages.warning(request, f'you Entered a Wrong OTP')
                return render(request, 'user/signup.html')
        else:

            firstname = request.POST['fname']
            # lastname=request.POST['lname']
            username = request.POST['username']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            context = {
                'pre_firstname': firstname,
                # 'pre_lastname':lastname,
                'pre_username': username,
                'pre_email': email,
                'pre_password1': password1,
                'pre_password2': password2
            }

            if username.strip() == '' or password1.strip() == '' or password2.strip() == '' or email.strip() == '' or firstname.strip() == '':
                messages.error(request, 'field cannot empty! ')
                return render(request, 'user/signup.html', context)

            elif User.objects.filter(username=username):
                messages.error(request, 'username alredy exist!')
                context['pre_username'] = ''
                return render(request, 'user/signup.html', context)

            elif not re.match(r'^[a-zA-Z\s]*$', username):
                messages.error(
                    request, 'Username should only contain alphabets!')
                context['pre_username'] = ''
                return render(request, 'user/signup.html', context)

            elif User.objects.filter(email=email):
                messages.error(request, 'email already exist!')
                context['pre_email'] = ''
                return render(request, 'user/signup.html', context)

            elif password1 != password2:
                messages.error(request, "password doesn't match")
                context['pre_password1'] = ''
                context['pre_password2'] = ''
                return render(request, 'user/signup.html', context)

            email_check = validateemail(email)
            if email_check is False:
                messages.error(request, 'email not valid!')
                context['pre_email'] = ''
                return render(request, 'user/signup.html', context)

            password_check = validatepassword(password1)
            if password_check is False:
                messages.error(request, 'Enter strong password!')
                context['pre_password1'] = ''
                context['pre_password2'] = ''
                return render(request, 'user/signup.html', context)

            user = User.objects.create_user(
                first_name=firstname, username=username, email=email, password=password1)
            user.is_active = False
            user.save()
            user_otp = random.randint(100000, 999999)
            UserOTP.objects.create(user=user, otp=user_otp)
            mess = f'Hello \t{user.username},\nYour OTP to verify your account for Confirmation {user_otp}\n Thanks You!'
            send_mail(
                "Welcome to MS Sounds , verify your Email",
                mess,
                settings.EMAIL_HOST_USER,
                [user.email],

                fail_silently=False


            )

            return render(request, 'user/signup.html', {'otp': True, 'user': user})

    return render(request, 'user/signup.html')


def validateemail(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def validatepassword(password1):
    try:
        validate_password(password1)
        return True
    except ValidationError:
        return False


def otp_verify(request):
    return render(request, 'otp.html')


def user_login1(request):
    if request.user.is_authenticated:
        return redirect('home')  # dashboard user

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if username.strip() == '' or password.strip() == '':
            messages.error(request, 'field cannot empty!')
            return redirect('user_login1')

        user = authenticate(username=username, password=password)

        if user is not None:

            if user.is_active:
                login(request, user)
                return redirect('home')  # dashboard user
            else:
                messages.warning(request, 'your account has been blocked!')
                return redirect('user_login1')

        else:
            messages.error(request, 'invalid username or password!')
            return redirect('user_login1')

    return render(request, 'user/login.html')


@login_required(login_url='user_login1')
def logout1(request):
    logout(request)
    return redirect('home')


def forgot_password(request):
    if request.method == 'POST':
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
                    return render(request, 'user/forgetsetup.html', {'otp': True, 'user': user, 'pre_otp': get_otp})

                elif password1 != password2:
                    messages.error(request, 'Password does not match!')
                    return render(request, 'user/forgetsetup.html', {'otp': True, 'user': user, 'pre_otp': get_otp})

                Pass = validatepassword(password1)
                if Pass is False:
                    messages.error(request, 'Please enter Strong password!')
                    return render(request, 'user/forgetsetup.html', {'otp': True, 'user': user, 'pre_otp': get_otp})
                user.set_password(password1)
                user.save()
                UserOTP.objects.filter(user=user).delete()
                return redirect('user_login1')
            else:
                messages.warning(request, 'You Entered a wrong OTP!')
                return render(request, 'user/forgetsetup.html', {'otp': True, 'user': user})

        else:
            email = request.POST['email']

            if email.strip() == '':
                messages.error(request, 'field cannot empty!')
                return render(request, 'user/forgetsetup.html')

            email_check = validateemail(email)
            if email_check is False:
                messages.error(request, 'email not valid!')
                return render(request, 'user/forgetsetup.html')

            if User.objects.filter(email=email):
                user = User.objects.get(email=email)
                user_otp = random.randint(100000, 999999)
                UserOTP.objects.create(user=user, otp=user_otp)
                message = f'Hello\t{user.username},\n Your OTP to verify your account for MS Sounds is {user_otp}\n Thanks'
                send_mail(
                    "welcome to Coot Verify Email",
                    message,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False
                )
                return render(request, 'user/forgetsetup.html', {'otp': True, 'user': user})
            else:
                messages.error(request, 'email does not exist!')
                return render(request, 'user/forgetsetup.html')
    return render(request, 'user/forgetsetup.html')
