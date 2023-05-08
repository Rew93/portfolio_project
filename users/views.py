from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models.query_utils import Q
from django.shortcuts import HttpResponseRedirect, render, reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from blog.models import BlogModel, CategoryModel, CommentsModel
from users.forms import (ChangePasswordForm, LoginForm, NewPasswordForm,
                         ProfileForm, RegisterForm, ResetPasswordForm)
from users.token import account_activation_token

# Create your views here.
popular_blog = sorted(BlogModel.objects.all(), key=lambda x: x.count_comment, reverse=True)
category = CategoryModel.objects.all()
recent_comments = sorted(CommentsModel.objects.filter(parent=None), key=lambda x: len(x.children), reverse=True)


def login_register(request):
    if request.method == 'POST':
        if 'login_form' in request.POST:
            login_form = LoginForm(data=request.POST)
            register_form = RegisterForm()
            if login_form.is_valid():
                username = request.POST['username']
                password = request.POST['password']
                user = auth.authenticate(username=username, password=password)
                if user:
                    auth.login(request, user)
                    messages.success(request, f'Hello, {user.get_full_name()}. You have bin logged in.')
                    return HttpResponseRedirect(reverse('blogs'))
            else:
                for key, error in list(login_form.errors.items()):
                    if key == 'captcha' and error[0] == 'This field is required.':
                        messages.error(request, 'You must pass the reCaptcha test')
                        continue
                    messages.error(request, error)
        elif 'register_form' in request.POST:
            register_form = RegisterForm(data=request.POST)
            login_form = LoginForm()
            if register_form.is_valid():
                user = register_form.save(commit=False)
                user.is_verified = False
                user.save()
                mail_subject = 'The Activation link has been sent to your email address'
                message = render_to_string('users/acc_active_email.html', {
                    'user': user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                    'protocol': 'https' if request.is_secure() else 'http',
                })
                to_email = register_form.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                messages.success(request, f'Hello {user.get_full_name()}.'
                                          f'Please proceed confirm your email address ({user.email}) to complete the registration.')
                # return render(request, 'users/verification_email.html', context)

            else:
                for error in list(register_form.errors.values()):
                    messages.error(request, error)
    else:
        login_form = LoginForm()
        register_form = RegisterForm()
    context = {
        'categories': category,
        'popular_blog': popular_blog[:5],
        'popular_blog_2': popular_blog[:2],
        'recent_comments': recent_comments[:5],
        'login_form': login_form,
        'register_form': register_form,
    }
    return render(request, 'users/login_register.html', context)


@login_required(login_url='login_register')
def logout(request):
    auth.logout(request)
    messages.success(request, 'Logout')
    return HttpResponseRedirect(reverse('login_register'))


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_verified = True
        user.save()
        context = {'user': user}
        return render(request, 'users/email_confirmation.html', context)
    else:
        return render(request, 'users/link_invalid.html')


@login_required(login_url='login_register')
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f'{request.user}, You profile has been updated!')
            return HttpResponseRedirect(reverse('profile'))
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = ProfileForm(instance=request.user)
    context = {
        'form': form,
        'categories': category,
        'popular_blog': popular_blog[:5],
        'popular_blog_2': popular_blog[:2],
        'recent_comments': recent_comments[:5],
    }
    return render(request, 'users/profile.html', context)


@login_required(login_url='login_register')
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(user, data=request.POST)
        if form.is_valid() and form.cleaned_data['old_password'] != form.cleaned_data['new_password1']:
            form.save()
            messages.success(request, 'Your password has been changed')
            return HttpResponseRedirect(reverse('login_register'))
        else:
            if form.cleaned_data['old_password'] == form.cleaned_data['new_password1']:
                messages.error(request, 'Your password old reply new')
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = ChangePasswordForm(user)
    context = {
        'form': form,
        'categories': category,
        'popular_blog': popular_blog[:5],
        'popular_blog_2': popular_blog[:2],
        'recent_comments': recent_comments[:5],
    }
    return render(request, 'users/password_change_confirmation.html', context)


def password_reset(request):
    if request.method == 'POST':
        form = ResetPasswordForm(data=request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = 'Password Reset'
                message = render_to_string('users/acc_reset_password.html', {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    'protocol': 'https' if request.is_secure() else 'http',
                })
                email = EmailMessage(
                    subject, message, to=[user_email]
                )
                email.send()
                if email.send():
                    messages.success(request,
                                     """
                                     <h2>Password reset send</h2><br>
                                     <p>We are emailed instructions to setting your password, if an account exist with your email you entered.
                                        You should receive them shortly.<br>If your don`t receive an email, please make sure you`ve entered the address 
                                        you register with,and check your spam folder. 
                                     </p>
                                     """)
                else:
                    messages.error(request, 'Problem sending reset password email, <b>SERVER PROBLEM</>')
            return HttpResponseRedirect(reverse('login_register'))
        for key, error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(request, 'You must pass the reCaptcha test')
                continue
            messages.error(request, error)

    form = ResetPasswordForm()
    context = {
        'form': form,
        'categories': category,
        'popular_blog': popular_blog[:5],
        'popular_blog_2': popular_blog[:2],
        'recent_comments': recent_comments[:5],
    }
    return render(request, 'users/password_reset.html', context)


def new_password(request):
    user = request.user
    if request.method == 'POST':
        form = NewPasswordForm(user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password has been changed')
            return HttpResponseRedirect(reverse('login_register'))
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = NewPasswordForm(user)
    context = {
        'form': form,
        'categories': category,
        'popular_blog': popular_blog[:5],
        'popular_blog_2': popular_blog[:2],
        'recent_comments': recent_comments[:5],
    }
    return render(request, 'users/new_password.html', context)


def password_reset_confirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        if request.POST == 'POST':
            form = NewPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'You password has been set. You may go ahead and log in now.')
                return HttpResponseRedirect(reverse('login_register'))
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
        form = NewPasswordForm(user)
        context = {
            'form': form,
            'categories': category,
            'popular_blog': popular_blog[:5],
            'popular_blog_2': popular_blog[:2],
            'recent_comments': recent_comments[:5],
        }
        return render(request, 'users/new_password.html', context)
    else:
        messages.error(request, 'Link is expired')
    messages.error(request, 'Something went wrong, redirecting back ti login-register page')
    return HttpResponseRedirect(reverse('login_register'))
