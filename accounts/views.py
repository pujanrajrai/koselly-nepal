import string
import random
from datetime import datetime, timezone
from random import randint
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, HttpResponse, redirect
from .models import MyUser, EmailVerification
from .forms import MyUserCreationForm, ChangePasswordForm
from django.core.mail import send_mail
from ecommerce.settings import EMAIL_HOST_USER


# Create your views here.


def register(request):
    if request.user.is_authenticated:
        if request.user:
            return redirect('home:home')
    context = {'form': MyUserCreationForm()}
    if request.method == 'POST':
        email = request.POST.get('email')
        context['email'] = email
        if request.user.is_authenticated:
            return redirect('/')
        form = MyUserCreationForm(request.POST)
        username = request.POST.get('username')
        password1 = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password1 != password2:
            context['errors'] = 'Password and conform Password didnot match'
            context['email'] = request.POST['email']
            context['username'] = username
            return render(request, 'accounts/register.html', context)
        if form.is_valid():
            form.save()
            email = email
            password = password1
            user = auth.authenticate(email=email, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('accounts:send_email_verification_code')
            else:

                context['errors'] = "something went wrong"
                return render(request, 'accounts/login.html', context)
        else:
            context['errors'] = form.errors
            context['email'] = request.POST['email']
            context['username'] = username

    return render(request, 'accounts/register.html', context)


# sending email verification code
@login_required()
def send_email_verification_code(request):
    user = request.user
    if MyUser.objects.get(email=request.user).is_email_verified:
        return HttpResponse('email already Verified')
    code = randint(100000, 999999)  # verification code
    create_date = datetime.now()
    total_try_requests = 0

    if not EmailVerification.objects.filter(users=user).exists():
        EmailVerification.objects.create(
            users=user,
            verification_code=code,
            created_date_time=create_date,
            total_try_request=total_try_requests,
        )
    else:
        email_verification = EmailVerification.objects.get(users=user)
        block_date = email_verification.block_time
        now = datetime.now(timezone.utc)
        difference = now - block_date
        if difference.total_seconds() < 300:
            return HttpResponse(f'You have been block for {difference} second')
        EmailVerification.objects.filter(users=user).update(
            verification_code=code,
            created_date_time=create_date,
            total_try_request=total_try_requests,
        )
    send_mail(
        "Email Verification Code",
        f"Your email verification code is {code}",
        EMAIL_HOST_USER,
        [EmailVerification.objects.get(users=user).users.email],
    )
    return redirect('accounts:verify_email')


@login_required()
def verify_email(request):
    if MyUser.objects.get(email=request.user).is_email_verified:
        return redirect('my_profile:profile_create')
    if request.method == 'POST':
        if MyUser.objects.get(email=request.user).is_email_verified:
            return redirect('my_profile:profile_create')

        request_code = request.POST['otp1'] + request.POST['otp2'] + request.POST['otp3'] + request.POST['otp4'] + \
            request.POST['otp5'] + \
            request.POST['otp6']  # code send from user to verify
        code = EmailVerification.objects.get(
            users=request.user).verification_code
        if request_code == code:
            MyUser.objects.filter(email=request.user).update(
                is_email_verified=True)
            return redirect('my_profile:profile_create')
        else:
            context = {'error': 'code you have entered is wrong'}
            return render(request, 'accounts/verify_email.html', context)
    return render(request, 'accounts/verify_email.html')


def login(request):
    if request.user.is_authenticated:
        if request.user:

            return redirect('my_profile:profile_create')
            # return redirect('dashboard:')
    if request.method == 'POST':
        if request.user.is_authenticated:
            if request.user:
                # return redirect('my_profile:profile_create')
                return redirect('home:home')
            else:
                # return redirect('my_profile:profile_create')
                return redirect('home:home')
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            context = {"errors": "User name or password is incorrect",
                       "email": request.POST['email']}
            return render(request, 'accounts/logi'
                                   'n.html', context)

        # if request.user:
        #     return redirect('my_profile:profile_create')

        #     # return redirect('home:home')
        # else:
        #     return redirect('my_profile:profile_create')

            # return redirect('home:home')
    return render(request, 'accounts/login.html')


@login_required()
def password_change(request):
    context = {}
    if request.method == 'POST':
        old_password = request.POST['old_password']
        password = request.POST['password']
        password2 = request.POST['password2']
        data = {"password": password, 'password2': password2,
                "old_password": old_password}

        if not request.user.check_password(old_password):
            context['errors'] = 'Your password didnot match with old password'
        if old_password == password:
            context['errors'] = 'old password cannot be new password'
        if password != password2:
            context['errors'] = 'your conformed password didnot matched'
        form = ChangePasswordForm(data)
        if form.is_valid():
            MyUser.objects.filter(email=request.user).update(
                password=make_password(form.data['password']))
        else:
            context['errors'] = form.errors
    return render(request, 'accounts/change_password.html', context)


def logout(request):
    auth.logout(request)
    return redirect('/')


def forger_password(request):
    context = {}
    if request.method == 'POST':
        email = request.POST['email']
        length = 10
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        num = string.digits
        symbols = string.punctuation
        all = lower + upper + num + symbols
        temp = random.sample(all, length)
        password = "".join(temp)
        send_mail(
            "Email Verification Code",
            f"Your email verification code is {password}",
            EMAIL_HOST_USER,
            [email],
        )
        MyUser.objects.filter(email=email).update(
            password=make_password(password))
        context['errors'] = 'Password has been send to your email address'
    return render(request, 'accounts/forget_password.html', context)
