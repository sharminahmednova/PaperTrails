from django.shortcuts import render, redirect
from user_authintication.forms import RecentProduct
from django.http import HttpResponseRedirect, JsonResponse
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
from pages.models import Book, DonateBook, DonateBookRequest, LendBorrow, BorrowRequest
from user_authintication.forms import BookForm, LendBorrowForm, BorrowRequestForm, DonateBookForm, DonateBookRequestForm
import json
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




@user_passes_test(lambda u: u.is_authenticated, login_url='/')
def DashboardPage(request):

    if not request.user.is_authenticated:
        messages.info(request, "Not authorized ! Login first")
        return redirect('/')
    

    return render(request, 'dashboard.html', {})

@user_passes_test(lambda u: u.is_authenticated, login_url='/')
def PersonalBookPage(request):

    if not request.user.is_authenticated:
        messages.info(request, "Not authorized ! Login first")
        return redirect('/')

    books = Book.objects.filter(owner=request.user)

    return render(request, 'personalBookPage.html', {'books': books})

@user_passes_test(lambda u: u.is_authenticated, login_url='/')
def AddPersonalBookPage(request):

    form = BookForm()

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)

        if form.is_valid():
            book = form.save(commit=False)
            book.owner = request.user
            book.save()

            messages.success(request, 'Book added successfully !')

            return redirect('/')
        else:
            messages.error(request, 'Invalid form submission !')

    return render(request, 'addPersonalBook.html', {'form': form})


def EditPersonalBookPage(request, id):

    book = Book.objects.get(id=int(id))

    form = BookForm(instance=book)

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)


        if form.is_valid():
            book.owner = request.user
            book.author = book.author
            book.name = book.name
            book.description = book.description
            book.genre = book.genre
            book.subject = book.subject
            book.language = book.language
            book.condition = book.condition
            book.price = book.price
            book.location = book.location
            if request.FILES.get('book_image') is not None:
                book.book_image = request.FILES['book_image']

            book.save()

            messages.success(request, 'Book updated successfully !')
            return redirect('/')
        else:
            messages.error(request, 'Invalid form submission !')

    return render(request, 'addPersonalBook.html', {'form': form})


def DeleteBook(request, id):

    book = Book.objects.get(id=int(id))

    if request.method == 'POST':
        if book.owner != request.user:
            messages.error(request, 'You are not authorized to delete this book !')
            return redirect('/')

        book.delete()
        messages.success(request, 'Book deleted successfully !')
        return redirect('/')

    return render(request, 'deleteBook.html', {'book': book})



@user_passes_test(lambda u: u.is_authenticated, login_url='/')
def LendBookFormPage(request):

    form = LendBorrowForm() 

    books = [book for book in Book.objects.filter(owner=request.user) if book.is_free]


    for book in books:
        print(book.is_free)

    if request.method == 'POST':
        bookId = request.POST['book']
        lend_duration = request.POST['lend_duration']

        if LendBorrow.objects.filter(book=bookId).exists():
            messages.error(request, "The book is listed already for lending")
            return redirect('/')

        lendBook = LendBorrow.objects.create(
            book=Book.objects.get(id=int(bookId)),
            lender=request.user.profile,
            lend_duration=int(lend_duration),
        )

        messages.success(request, 'Book lend add published successfully !')
        return redirect('/')


    return render(request, 'lend_borrow.html', {'form': form, 'books': books})



@user_passes_test(lambda u: u.is_authenticated, login_url='/')
def BorrowInsidePage(request, id):

    lendBorrow = LendBorrow.objects.get(id=int(id))

    duration = lendBorrow.lend_duration

    form = BorrowRequestForm()

    if request.method == 'POST':
        requestMessage = request.POST['request_message']
        requestDuration = request.POST['borrow_duration']

        print(requestMessage, requestDuration)

        borrowRequest = BorrowRequest.objects.create(
            request_message=requestMessage, request_duration=int(requestDuration),
            lendBorrow=lendBorrow,
            borrower=request.user.profile
            )
        
        borrowRequest.save()
        messages.success(request, 'Borrow request sent successfully !')
        return redirect('/')

    return render(request, 'borrow_inside.html', {'form': form, 'duration': duration})



def ManageBorrowRequest(request):
    borrowRequests = BorrowRequest.objects.select_related('lendBorrow').filter(lendBorrow__lender=request.user.profile).filter(rejected=False)

    return render(request, 'manage_borrow_request.html', {'borrowRequests': borrowRequests})

def ManageBorrowRequestInside(request, id):

    borrowRequest = BorrowRequest.objects.select_related('lendBorrow').get(id=int(id))

    if request.method == 'POST':
    
        accept = request.POST.get('accept')
        reject = request.POST.get('reject')

        delete = request.POST.get('delete')

        print(accept, reject, delete)

        if accept == 'accept':

            lendBorrow = LendBorrow.objects.get(id=borrowRequest.lendBorrow.id)
            lendBorrow.lend_status = True
            lendBorrow.borrower = borrowRequest.borrower
            lendBorrow.save()

            borrowRequest.accepted = True
            borrowRequest.rejected = False
            borrowRequest.save()

            messages.success(request, 'Borrow request accepted !')
            return redirect('/')

        elif reject == 'reject':
            borrowRequest.accepted = False
            borrowRequest.rejected = True
            borrowRequest.save()

            messages.success(request, 'Borrow request rejected !')
            return redirect('/')
        
        elif delete == 'delete':
            print('Delete triggered')
            # borrowRequest.lendBorrow.delete()

            LendBorrow.objects.get(id=borrowRequest.lendBorrow.id).delete()
            # borrowRequest.delete()
            messages.success(request, 'Borrow request deleted !')
            return redirect('/')


    return render(request, 'manage_borrow_request_inside.html', {'borrowRequest': borrowRequest})


def ManageBorrowedBooks(request):

    borrowedBooks = BorrowRequest.objects.select_related('lendBorrow__book__owner__profile').filter(borrower=request.user.profile).filter(accepted=True)

    # for borrowedBook in borrowedBooks:
    #     print(borrowedBook.lendBorrow.book.owner.profile.name)
    #     print(borrowedBook.lendBorrow.lender.profileUser.username)
    #     print(borrowedBook.request_duration)

    if request.method == 'POST':
        data = json.loads(request.body)

        id = data['id']
        borrowRequest = BorrowRequest.objects.get(id=int(id))

        borrowRequest.return_status = True
        borrowRequest.save()


        return JsonResponse({'success':True})
        




    return render(request, 'manage_borrowed_books.html', {'borrowedBooks': borrowedBooks})





@user_passes_test(lambda u: u.is_authenticated, login_url='/')
def DonateBookFormPage(request):

    form = LendBorrowForm() 

    books = [book for book in Book.objects.filter(owner=request.user) if book.is_free]


    for book in books:
        print(book.is_free)

    if request.method == 'POST':
        bookId = request.POST['book']
        
        donateBook = DonateBook.objects.create(
            book=Book.objects.get(id=int(bookId)),
            owner=request.user.profile,
        )


        messages.success(request, 'Book donation add published successfully !')
        return redirect('/')


    return render(request, 'donateBook.html', {'form': form, 'books': books})




@user_passes_test(lambda u: u.is_authenticated, login_url='/')
def DonationInsidePage(request, id):

    donateBook = DonateBook.objects.get(id=int(id))


    form = DonateBookRequestForm()

    if request.method == 'POST':
        requestMessage = request.POST['request_message']

        print(requestMessage)

        donateBookRequest = DonateBookRequest.objects.create(
            request_message=requestMessage,
            donateBook=donateBook,
            requestor=request.user.profile,
            request_status=True,
            )
        
        messages.success(request, 'Donation request sent successfully !')
        return redirect('/')

    return render(request, 'donate_inside.html', {'form': form})



def ManageDonateRequest(request):
    donateRequests = DonateBookRequest.objects.select_related('donateBook__book').filter(donateBook__owner=request.user.profile).filter(rejected=False)

    for donateRequest in donateRequests:
        print(donateRequest.donateBook.book.name)
        print(donateRequest.requestor.profileUser.username)
        print(donateRequest.request_message)

    return render(request, 'manage_donation_requests.html', {'donateRequests': donateRequests})


def ManageDonateRequestInside(request, id):
    donateRequest = DonateBookRequest.objects.select_related('donateBook__book').get(id=int(id))

    if request.method == 'POST':
    
        accept = request.POST.get('accept')
        reject = request.POST.get('reject')

        delete = request.POST.get('delete')


        print(accept, reject, delete)

        if accept == 'accept':
            donateRequest = DonateBookRequest.objects.get(id=donateRequest.id)
            donateRequest.accepted = True
            donateRequest.rejected = False
            # donateRequest.donateBook.request_status = True
            donateRequest.save()


            donateBook = donateRequest.donateBook
            donateBook.requestor = donateRequest.requestor
            donateBook.donate_status = True
            donateBook.save()

            print(donateBook)

            messages.success(request, 'Donation request accepted !')
            return redirect('/')

        elif reject == 'reject':
            donateRequest.accepted = False
            donateRequest.rejected = True
            donateRequest.save()
            messages.success(request, 'Donation request rejected !')
            return redirect('/')
        
        elif delete == 'delete':
            book = donateRequest.donateBook.book
            book.owner = donateRequest.requestor.profileUser
            book.save()
            donateRequest.donateBook.delete()
            messages.success(request, 'Donation request deleted !')
            return redirect('/')



    return render(request, 'manage_donation_requests_inside.html', {'donateRequest': donateRequest})








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