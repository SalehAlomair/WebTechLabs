from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q, Count, Sum, Avg, Max, Min, OuterRef, Subquery
from .models import Book, Student, Publisher, Author

def index(request):
    return render(request, "bookmodule/index.html")

def list_books(request):
    return render(request, 'bookmodule/list_books.html')


def index2(request, val1=0):
    return HttpResponse("value1 = " + str(val1))

def viewbook(request, bookId):
    return render(request, 'bookmodule/one_book.html')

def aboutus(request):
    return render(request, 'bookmodule/aboutus.html')


def html5_links(request):
    return render(request, 'bookmodule/html5_links.html')


def html5_text_formatting(request):
    return render(request, 'bookmodule/html5_text_formatting.html')


def html5_listing(request):
    return render(request, 'bookmodule/html5_listing.html')


def html5_tables(request):
    return render(request, 'bookmodule/html5_tables.html')


def __getBooksList():
    book1 = {'id': 12344321, 'title': 'Continuous Delivery', 'author': 'J.Humble and D. Farley'}
    book2 = {'id': 56788765, 'title': 'Reversing: Secrets of Reverse Engineering', 'author': 'E. Eilam'}
    book3 = {'id': 43211234, 'title': 'The Hundred-Page Machine Learning Book', 'author': 'Andriy Burkov'}
    return [book1, book2, book3]


def search(request):
    if request.method == 'POST':
        string = (request.POST.get('keyword') or '').lower()
        isTitle = request.POST.get('option1')
        isAuthor = request.POST.get('option2')

        books = __getBooksList()
        newBooks = []
        for item in books:
            contained = False
            if isTitle and string in item['title'].lower():
                contained = True
            if not contained and isAuthor and string in item['author'].lower():
                contained = True
            if contained:
                newBooks.append(item)

        return render(request, 'bookmodule/bookList.html', {'books': newBooks})

    return render(request, 'bookmodule/search.html')


def simple_query(request):
    mybooks = Book.objects.filter(title__icontains='and')
    return render(request, 'bookmodule/bookList.html', {'books': mybooks})


def complex_query(request):
    mybooks = Book.objects.filter(
        author__isnull=False
    ).filter(
        title__icontains='and'
    ).filter(
        edition__gte=2
    ).exclude(
        price__lte=100
    )[:10]

    if len(mybooks) >= 1:
        return render(request, 'bookmodule/bookList.html', {'books': mybooks})
    return render(request, 'bookmodule/index.html')


def lab8_task1(request):
    books = Book.objects.filter(Q(price__lte=80))
    return render(request, 'bookmodule/lab8_books_list.html', {'books': books, 'task_title': 'Lab8 Task1'})


def lab8_task2(request):
    books = Book.objects.filter(
        Q(edition__gt=3) & (Q(title__icontains='qu') | Q(author__icontains='qu'))
    )
    return render(request, 'bookmodule/lab8_books_list.html', {'books': books, 'task_title': 'Lab8 Task2'})


def lab8_task3(request):
    books = Book.objects.filter(
        Q(edition__lte=3) & (~Q(title__icontains='qu') | ~Q(author__icontains='qu'))
    )
    return render(request, 'bookmodule/lab8_books_list.html', {'books': books, 'task_title': 'Lab8 Task3'})


def lab8_task4(request):
    books = Book.objects.order_by('title')
    return render(request, 'bookmodule/lab8_books_list.html', {'books': books, 'task_title': 'Lab8 Task4'})


def lab8_task5(request):
    stats = Book.objects.aggregate(
        number_of_books=Count('id'),
        total_price=Sum('price'),
        average_price=Avg('price'),
        max_price=Max('price'),
        min_price=Min('price'),
    )
    return render(request, 'bookmodule/lab8_task5.html', {'stats': stats})


def lab8_task7(request):
    city_counts = Student.objects.values('address__city').annotate(num_students=Count('id')).order_by('address__city')
    return render(request, 'bookmodule/lab8_task7.html', {'city_counts': city_counts})


def lab9_task1(request):
    books = Book.objects.filter(publisher__isnull=False).order_by('id')
    total_books = books.aggregate(total=Sum('quantity'))['total'] or 0
    for book in books:
        book.percentage = round((book.quantity / total_books) * 100) if total_books else 0
    return render(request, 'bookmodule/lab9_task1.html', {'books': books})


def lab9_task2(request):
    publishers = Publisher.objects.annotate(total_stock=Sum('books__quantity')).order_by('name')
    return render(request, 'bookmodule/lab9_task2.html', {'publishers': publishers})


def lab9_task3(request):
    oldest_books = Book.objects.filter(publisher=OuterRef('pk')).order_by('pubdate')
    publishers = Publisher.objects.annotate(
        oldest_title=Subquery(oldest_books.values('title')[:1]),
        oldest_pubdate=Subquery(oldest_books.values('pubdate')[:1]),
    ).order_by('name')
    return render(request, 'bookmodule/lab9_task3.html', {'publishers': publishers})


def lab9_task4(request):
    publishers = Publisher.objects.annotate(
        avg_price=Avg('books__price'),
        min_price=Min('books__price'),
        max_price=Max('books__price'),
    ).order_by('name')
    return render(request, 'bookmodule/lab9_task4.html', {'publishers': publishers})


def lab9_task5(request):
    publishers = Publisher.objects.annotate(
        high_rated_count=Count('books', filter=Q(books__rating__gte=4))
    ).order_by('name')
    return render(request, 'bookmodule/lab9_task5.html', {'publishers': publishers})


def lab9_task6(request):
    publishers = Publisher.objects.annotate(
        filtered_count=Count(
            'books',
            filter=Q(books__price__gt=50, books__quantity__lt=5, books__quantity__gte=1)
        )
    ).order_by('name')
    return render(request, 'bookmodule/lab9_task6.html', {'publishers': publishers})
