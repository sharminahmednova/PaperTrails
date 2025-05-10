from django.shortcuts import render, redirect
from pages.models import Book, DonateBook, LendBorrow, Wishlist, Bid, WishlistItem
from django.db.models import Max, Min
from django.template.loader import render_to_string
import json
from django.http import JsonResponse
from user_authintication.models import Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def HomePage(request):
    return render(request, 'home.html', {})

@login_required
def BookListingPage(request):
    books = Book.objects.all()
    wishlist_items = WishlistItem.objects.filter(user_name=request.user.username)
    wishlist_book_ids = list(wishlist_items.values_list('book_id', flat=True))

    if request.method == 'POST':
        data = json.loads(request.body)
        conditions = data['conditions']
        locations = data['locations']
        price = data['price']

        if len(conditions) > 0:
            books = books.filter(condition__in=conditions)
        if len(locations) > 0:
            books = books.filter(location__in=locations)
        if price:
            books = books.filter(price__lte=int(price))
        
        updated_html = render_to_string('bookListingContainer.html', {
            'books': books,
            'user': request.user,
            'wishlist_book_ids': wishlist_book_ids
        })
        return JsonResponse({'updated_html': updated_html})

    maxPrice = Book.objects.aggregate(Max('price'))
    minPrice = Book.objects.aggregate(Min('price'))
    conditions = ['New', 'Used but like new', 'Used']
    locations = ['Dhaka', 'Rajshahi', 'Khulna']

    return render(request, 'bookListing.html', {
        "books": books,
        "maxPrice": maxPrice,
        "minPrice": minPrice,
        'conditions': conditions,
        'locations': locations,
        'user': request.user,
        'wishlist_book_ids': wishlist_book_ids
    })

def BookListingPageFilter(request):
    data = json.loads(request.body)
    conditions = data['conditions']
    locations = data['locations']
    price = data['price']
    pass

def BookDetailsPage(request, id):
    book = Book.objects.get(id=int(id))
    return render(request, 'bookDetails.html', {'book': book})


def LendBookPage(request):
    
    lendBooks = LendBorrow.objects.select_related('book__owner__profile').filter(lend_status=False)

    for lendBook in lendBooks:
        print(lendBook.id)
        print(lendBook.lendTitle)
        print(lendBook.lender.profileUser.username)

    return render(request, 'lendBook.html', {'lendBooks':lendBooks})


def DonateBookListPage(request):
    donateBooks = DonateBook.objects.select_related('book__owner__profile').filter(donate_status=False)

    for donateBook in donateBooks:
        print(donateBook.id)


    return render(request, 'donateBookListing.html', {'donateBooks':donateBooks})

@login_required
def WishlistPage(request):
    wishlist_items = WishlistItem.objects.filter(user_name=request.user.username)
    # Create a list of wishlist items with their corresponding book objects
    wishlist_data = []
    for item in wishlist_items:
        book = Book.objects.get(id=item.book_id)
        wishlist_data.append({
            'item': item,
            'book': book
        })
    return render(request, 'wishlist.html', {'wishlist_data': wishlist_data})

@login_required
def ToggleWishlist(request, book_id):
    book = Book.objects.get(id=book_id)
    user_name = request.user.username
    wishlist_item = WishlistItem.objects.filter(user_name=user_name, book_id=book_id).first()
    
    if wishlist_item:
        wishlist_item.delete()
        return JsonResponse({'status': 'removed'})
    else:
        WishlistItem.objects.create(
            book_name=book.name,
            user_name=user_name,
            book_id=book.id
        )
        return JsonResponse({'status': 'added'})

@login_required
def SubmitBid(request, book_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        bid_amount = int(data['bid_amount'])
        book = Book.objects.get(id=book_id)
        bidder = Profile.objects.get(profileUser=request.user)
        
        bid, created = Bid.objects.get_or_create(book=book, bidder=bidder, defaults={'amount': bid_amount})
        if not created:
            bid.amount = bid_amount
            bid.status = 'Pending'
            bid.save()
        
        owner = book.owner if hasattr(book, 'owner') else None
        if owner:
            messages.info(request, f'New bid of ${bid_amount} on your book "{book.name}" by {bidder.name}')
        
        return JsonResponse({'status': 'success', 'bid_amount': bid_amount})
    return JsonResponse({'status': 'error'}, status=400)