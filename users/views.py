from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test

from .forms import CustomUserCreationForm
from .tokens import AccountActivationTokenGenerator
from .models import CustomUser

token_generator = AccountActivationTokenGenerator()

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print('Form submitted:', request.method == 'POST')
        print('Form is valid:', form.is_valid())
        print('Form errors:', form.errors)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your Tosia account.'
            message = render_to_string('users/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            print('Sending email to:', to_email)
            print('Email subject:', mail_subject)
            print('Email message:', message)
            email = EmailMessage(
                mail_subject,
                message,
                to=[to_email]
            )
            email.content_subtype = "html"
            email.send()
            messages.success(request, 'Please confirm your email address to complete the registration.')
            return redirect('users:account_activation_sent')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def account_activation_sent(request):
    return render(request, 'users/account_activation_sent.html')

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        login(request, user)
        messages.success(request, 'Your account has been activated successfully!')
        return redirect('main:home')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('main:home')

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.info(request, f"You are now logged in as {username}.")
                    return redirect('main:home')
                else:
                    messages.error(request, "Please activate your account first. Check your email for activation link.")
                    return redirect('users:login')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('main:home')

def users_list(request):
    if not request.user.is_authenticated or not request.user.is_admin:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('main:home')
    users = CustomUser.objects.all()
    return render(request, 'users/users_list.html', {'users': users})

@login_required
@user_passes_test(lambda u: u.is_admin)
def add_admin_role(request, user_id):
    if request.method == 'POST':
        try:
            user = CustomUser.objects.get(id=user_id)
            user.is_admin = True
            user.save()
            messages.success(request, f"{user.username} is now an admin.")
        except CustomUser.DoesNotExist:
            messages.error(request, "User not found.")
    return redirect('users:users_list')

@login_required
@user_passes_test(lambda u: u.is_admin)
def remove_admin_role(request, user_id):
    if request.method == 'POST':
        try:
            user = CustomUser.objects.get(id=user_id)
            user.is_admin = False
            user.save()
            messages.success(request, f"{user.username} is no longer an admin.")
        except CustomUser.DoesNotExist:
            messages.error(request, "User not found.")
    return redirect('users:users_list')

@login_required
@user_passes_test(lambda u: u.is_admin)
def delete_user(request, user_id):
    if request.method == 'POST':
        try:
            user = CustomUser.objects.get(id=user_id)
            if user.id != request.user.id:  # Prevent self-deletion
                username = user.username
                user.delete()
                messages.success(request, f"User {username} has been deleted.")
            else:
                messages.error(request, "You cannot delete your own account.")
        except CustomUser.DoesNotExist:
            messages.error(request, "User not found.")
    return redirect('users:users_list')

@login_required
@user_passes_test(lambda u: u.is_admin)
def add_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"User {user.username} has been created.")
            return redirect('users:users_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/users_list.html', {'users': CustomUser.objects.all(), 'add_user_form': form})
