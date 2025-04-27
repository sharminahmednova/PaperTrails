from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages, auth
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from user_authintication.forms import RecentProduct, ProfileForm
from user_authintication.models import Profile
from .models import laptop
from .tokens import account_activation_token

# ---------------------- ACCOUNT ACTIVATION ----------------------
def ActivateAccount(request, user, toEmail):
    mail_subject = "Activate your account."
    message = render_to_string("activate_account_email.html", {
        'user': user.username,
        'domain': 'localhost:8000',
        'uid': user.id,
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[toEmail])

    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, Please check <b>{toEmail}</b> for activation link.')
    else:
        messages.error(request, "Activation email could not be sent.")

# ---------------------- LOGIN ----------------------
@user_passes_test(lambda u: not u.is_authenticated, login_url='/')
def LoginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            messages.info(request, "Login successful")

            # Admins redirect to admin dashboard, others to profile
            if user.is_staff:
                return redirect('/adminhome/')
            else:
                return redirect('/')

        messages.error(request, "Invalid credentials!")
    return render(request, 'login.html')

# ---------------------- REGISTRATION ----------------------
@user_passes_test(lambda u: not u.is_authenticated, login_url='/')
def RegisterPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
        elif password1 != password2:
            messages.error(request, 'Passwords do not match!')
        else:
            user = User.objects.create_user(username=username, first_name=name, email=email, password=password1)
            user.is_active = False
            user.save()
            Profile.objects.create(profileUser=user, name=name, email=email, phone=phone)
            ActivateAccount(request, user, email)
            return redirect('/')
    return render(request, 'register.html')

# ---------------------- ACTIVATE LINK ----------------------
def VerifyEmailActivateAccount(request, uidb64, token):
    User = get_user_model()
    try:
        user = User.objects.get(id=int(uidb64))
    except:
        user = None

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Account verified! Please login.')
        return redirect('login')
    messages.error(request, 'Invalid or expired activation link.')
    return redirect('/')

# ---------------------- LOGOUT ----------------------
def Logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        messages.info(request, "Logged out successfully")
    return redirect('/')

# ---------------------- PROFILE ----------------------
@login_required
def ProfilePage(request):
    if not request.user.is_authenticated:
        messages.info(request, "Not authorized ! Login first")
        return redirect('/')

    try:
        profile = request.user.profile
    except:
        if request.user.is_staff:
            return redirect('admin_profile')
        else:
            messages.error(request, "Profile not found.")
            return redirect('/')

    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        post_data = request.POST.copy()
        post_data['profileUser'] = request.user.id

        form = ProfileForm(instance=profile, data=post_data, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('/')

    return render(request, 'profile.html', {'form': form})

# ---------------------- PASSWORD RESET ----------------------
def ResetPassword1(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = get_user_model().objects.get(email=email)
        except:
            user = None
        if user:
            mail_subject = "Reset your password"
            message = render_to_string("password_reset_email.html", {
                'user': user.username,
                'domain': 'localhost:8000',
                'uid': user.id,
                'token': account_activation_token.make_token(user),
                'protocol': 'https' if request.is_secure() else 'http'
            })
            email = EmailMessage(mail_subject, message, to=[email])
            if email.send():
                messages.success(request, 'Password reset link sent to your email.')
            else:
                messages.error(request, 'Failed to send email.')
        else:
            messages.error(request, 'Email not found!')
    return render(request, 'reset_password1.html')

def ResetPassword2(request, uidb64, token):
    User = get_user_model()
    try:
        user = User.objects.get(id=int(uidb64))
    except:
        user = None

    if user and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if password1 != password2:
                messages.error(request, 'Passwords do not match!')
                return redirect('/')
            user.set_password(password1)
            user.save()
            messages.success(request, 'Password changed successfully!')
            return redirect('login')
        return render(request, 'reset_password2.html')
    messages.error(request, 'Invalid or expired password reset link')
    return redirect('/')

# ---------------------- FORM SUBMISSION ----------------------
def send(req):
    return render(req, 'user_auth/submit.html')

def details(request):
    if request.method == 'POST':
        frm = RecentProduct(request.POST)
        if frm.is_valid():
            cleaned = frm.cleaned_data
            laptop.objects.create(
                password=cleaned['password'],
                re_pass=cleaned['re_pass'],
                laptop=cleaned['laptop'],
                re_laptop=cleaned['re_laptop'],
                email=cleaned['email'],
                about=cleaned['about'],
                textarea=cleaned['textarea'],
                checkbox=cleaned['checkbox'],
                ram=cleaned['ram']
            )
            return HttpResponseRedirect('/auth/successfully')
    else:
        frm = RecentProduct()
    return render(request, 'user_auth/recent.html', {'form': frm})
