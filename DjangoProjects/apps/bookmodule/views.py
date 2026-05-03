from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Count, Sum, Avg, Max, Min, OuterRef, Subquery
from .models import Book, Student, Publisher, Author
from .forms import BookForm, BookFilterForm

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


def lab10_task1(request):
    books = Book.objects.select_related('publisher').prefetch_related('authors').order_by('id')
    return render(request, 'bookmodule/lab10_task1.html', {'books': books})


def lab10_task2(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('books.lab10.task1')
    else:
        form = BookForm()

    return render(request, 'bookmodule/lab10_task2.html', {'form': form})


def lab10_task3(request):
    book_id = request.GET.get('id')
    if not book_id:
        first_book = Book.objects.order_by('id').first()
        if not first_book:
            return render(request, 'bookmodule/lab10_task3.html', {'book': None, 'form': None})
        return redirect(f"/books/lab10/task3?id={first_book.id}")

    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('books.lab10.task1')
    else:
        form = BookForm(instance=book)

    return render(request, 'bookmodule/lab10_task3.html', {'book': book, 'form': form})


def lab10_task4(request):
    book_id = request.GET.get('id')
    if not book_id:
        return redirect('books.lab10.task1')

    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('books.lab10.task1')

    return render(request, 'bookmodule/lab10_task4.html', {'book': book})


def lab10_task5(request):
    form = BookFilterForm(request.GET or None)
    books = Book.objects.select_related('publisher').prefetch_related('authors').order_by('title')
    if form.is_valid():
        keyword = form.cleaned_data.get('keyword')
        min_price = form.cleaned_data.get('min_price')
        publisher = form.cleaned_data.get('publisher')

        if keyword:
            books = books.filter(Q(title__icontains=keyword) | Q(author__icontains=keyword))
        if min_price is not None:
            books = books.filter(price__gte=min_price)
        if publisher:
            books = books.filter(publisher=publisher)

    return render(request, 'bookmodule/lab10_task5.html', {'form': form, 'books': books})


def lab10_task6(request):
    created = False
    if request.method == 'POST':
        publisher, _ = Publisher.objects.get_or_create(name='Lab10 Publisher', defaults={'location': 'Doha'})
        author_a, _ = Author.objects.get_or_create(name='Lab10 Author A', defaults={'DOB': '1990-01-01'})
        author_b, _ = Author.objects.get_or_create(name='Lab10 Author B', defaults={'DOB': '1992-05-10'})

        for idx in range(1, 4):
            book, is_created = Book.objects.get_or_create(
                title=f'Lab10 Book {idx}',
                defaults={
                    'author': f'Author {idx}',
                    'price': 40 + idx * 10,
                    'edition': idx,
                    'quantity': idx + 1,
                    'rating': 3 + (idx % 2),
                    'publisher': publisher,
                },
            )
            if is_created:
                book.authors.add(author_a, author_b)
                created = True

    sample_books = Book.objects.filter(title__startswith='Lab10 Book').order_by('id')
    return render(request, 'bookmodule/lab10_task6.html', {'sample_books': sample_books, 'created': created})
