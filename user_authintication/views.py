from django.shortcuts import render, redirect
from user_authintication.forms import RecentProduct
from django.http import HttpResponseRedirect
from .models import laptop
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from user_authintication.models import Profile
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib import auth
from user_authintication.forms import ProfileForm
from django.contrib.auth.decorators import user_passes_test
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage

# Create your views here.

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

        messages.success(request, f'Dear <b>{user}</b>, Please go to your email <b>{toEmail}</b> inbox and click on the activation link to verify your Email. Note: Check your spam folder')

    else: 
        messages.error(request, "Mail could not be sent")

@user_passes_test(lambda u: not u.is_authenticated, login_url='/')
def LoginPage(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.info(request, "User login successful")

            return redirect('/')
        else: 
            messages.error(request, "Invalid credentials !")

    return render(request, 'login.html', {})

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
            messages.error(request, 'Username already exist !')

        elif password1 != password2:
            messages.error(request, 'Passwords do not match !')
        else: 

            user = User.objects.create_user(username=username, first_name=name, email=email, password=password1)

            user.is_active = False
            
            user.save()
            
            profile = Profile.objects.create(
                profileUser=user,
                name=name,
                email=email,
                phone=phone
            )

            ActivateAccount(request, user, email)

            return redirect('/')

    return render(request, 'register.html', {})


def VerifyEmailActivateAccount(request, uidb64, token):

    User = get_user_model()
    try: 
        user = User.objects.get(id=int(uidb64))
    
    except:
        user = None

    print(uidb64)
    print(token)
    print(user)

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True 
        user.save()

        messages.success(request, 'Account verified successfully ! Login now !')

        return redirect('login')

    else:
        messages.error(request, 'Account could not be verified. Invalid link or expired')


    return redirect('/')

def Logout(request):

    print('Logout def triggered')

    if (request.user.is_authenticated):
    
        auth.logout(request)
        messages.info(request, "Logout successful")

        return redirect('/')
    
    return redirect('/')



def ProfilePage(request):

    if not request.user.is_authenticated:
        messages.info(request, "Not authorized ! Login first")
        return redirect('/')


    form = ProfileForm(instance=request.user.profile)


    if request.method == 'POST':

        post_data = request.POST.copy()

        post_data['profileUser'] = request.user.id
        

        # print(post_data)

        form = ProfileForm(instance=request.user.profile, data= post_data, files=request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Updated successfully !')

            return redirect('/')



    context = {'form': form}

    return render(request, 'profile.html', context)



def ResetPassword1(request):


    if request.method == 'POST':

        email = request.POST['email']

        try:
            user = get_user_model().objects.get(email=email)
        except:
            user = None

        print(user.id)

        if user is not None:
            mail_subject = "Verify your email"

            message = render_to_string("password_reset_email.html", {
            'user': user.username,
            'domain': 'localhost:8000',
            'uid': user.id,
            'token': account_activation_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http'
            })

            email = EmailMessage(mail_subject, message, to=[email])

            if email.send():
                print("Inside RS1 Block")

                messages.success(request, 'An email has been sent to your account to reset your password.')
            else:
                messages.error(request, 'Email could not be sent')

        else:
            messages.error(request, 'Invalid email')



    return render(request,'reset_password1.html', {})



def ResetPassword2(request, uidb64, token):

    User = get_user_model()

    try:
        user = User.objects.get(id=int(uidb64))

    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):

        if request.method == 'POST':

            password1 = request.POST['password1']
            password2 = request.POST['password2']

            print(password1, password2)

            if password1 != password2:
                messages.error(request, 'Passwords do not match!')
                return redirect('/')

            user.set_password(password1)

            user.save()

            messages.success(request, 'Password changed successfully !')
            return redirect('login')
        
        return render(request, 'reset_password2.html', {})
    
    else:
        messages.error(request, 'Link expired or invalid link')
        # return redirect('/')
    
    
    
    
    return redirect('/')








def send(req):
    return render(req,'user_auth/submit.html')
def details(request):
    if request.method == 'POST':
        frm= RecentProduct(request.POST)
        if frm.is_valid():
            print('Valid form')
            pas=frm.cleaned_data['password']
            rpas=frm.cleaned_data['re_pass']
            lap=frm.cleaned_data['laptop']
            rlap=frm.cleaned_data['re_laptop']
            eml=frm.cleaned_data['email']
            abt=frm.cleaned_data['about']
            txt=frm.cleaned_data['textarea']
            chk=frm.cleaned_data['checkbox']
            rm=frm.cleaned_data['ram']
            
            buy=laptop(password=pas,re_pass=rpas,laptop=lap,re_laptop=rlap,email=eml,about=abt,textarea=txt,checkbox=chk,ram=rm)
            buy.save()

            return HttpResponseRedirect('/auth/successfully')
        else:
            frm= RecentProduct(auto_id=True,label_suffix=' - ')
            print('GET Statement')
    frm = RecentProduct()
    return render(request, 'user_auth/recent.html',{'form' : frm})