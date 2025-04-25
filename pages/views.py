from django.shortcuts import render
from pages.models import Book, DonateBook, LendBorrow
from django.db.models import Max, Min
from django.template.loader import render_to_string
import json
from django.http import JsonResponse
# Create your views here.
def HomePage(request):

        
    return render(request, 'home.html', {})


def BookListingPage(request):

    books = Book.objects.all()


    print(books)

    if request.method == 'POST':
        data = json.loads(request.body)
        conditions = data['conditions']
        locations = data['locations']
        price = data['price']

        print(conditions, locations, price)

        print(type(price))


        if len(conditions) > 0:
            books = books.filter(condition__in=conditions)
        if len(locations) > 0:
            books = books.filter(location__in=locations)
        if price:
            # books = books.filter(price=int(price))
            print(books)

            books = books.filter(price__lte=int(price))
        
        updated_html = render_to_string('bookListingContainer.html', {'books':books})

        print(books)
 
        return JsonResponse({'updated_html':updated_html})


    maxPrice = Book.objects.aggregate(Max('price'))
    minPrice = Book.objects.aggregate(Min('price'))

    conditions = ['New', 'Used but like new', 'Used']
    locations = ['Dhaka', 'Rajshahi', 'Khulna']



    return render(request, 'bookListing.html', {"books":books, "maxPrice": maxPrice, "minPrice": minPrice, 'conditions': conditions, 'locations': locations})






def BookDetailsPage(request, id):

    book = Book.objects.get(id=int(id))

    return render(request, 'bookDetails.html', {'book':book})


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