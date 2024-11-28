from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from rest_framework import generics
from rest_framework.views import APIView, View
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Book, UserBooks
from .serializers import BookSerializer, RegisterSerializer
from .decorators import jwt_required
from .forms import BookForm


class BookAPIViewPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10000


class BookAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = BookAPIViewPagination


class BookAPIUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserBooks.objects.all()
    serializer_class = BookSerializer
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAuthenticated, )


class AddToCollectionAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, book_id):
        user = request.user
        try:
            book = Book.objects.get(id=book_id)
            UserBooks.objects.get_or_create(user=user, book=book)
            return Response({"message": "Книга успешно добавлена в коллекцию!"}, status=201)
        except Book.DoesNotExist:
            return Response({"error": "Книга не найдена"}, status=404)
        

class RegisterView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def get(self, request, *args, **kwargs):
        context = {
            'title': 'Регистрация',
        }
        return render(request, 'register.html', context)  
    
    def post(self, request, *args, **kwargs):
        print('Request data:', request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Регистрация прошла успешно"}, status=201)
        print(serializer.errors)
        return Response(serializer.errors, status=400)


def BaseView(request):
    context = {
        'title': 'Главная',
    }
    return render(request, 'index.html', context)


def AboutUsView(request):
    context = {
        'title': 'О нас'
    }
    return render(request, 'about_us.html', context)


@jwt_required
def BooksView(request):
    jwt_authenticator = JWTAuthentication()
    try:
        user, _ = jwt_authenticator.authenticate(request)
    except Exception:
        return redirect('/login/')  

    if not user or user.is_anonymous:
        return redirect('/login/') 

    books = Book.objects.all()
    return render(request, 'allbooks.html', {'books': books, 'title': 'Все книги'})


@jwt_required
def UserBooksView(request):
    jwt_authenticator = JWTAuthentication()
    try:
        user, _ = jwt_authenticator.authenticate(request)
    except Exception:
        return redirect('/login/')  

    if not user or user.is_anonymous:
        return redirect('/login/') 

    user_books = UserBooks.objects.filter(user=user).select_related('book')
    return render(request, 'mybooks.html', {
        'title': 'Мои книги',
        'user_books': [user_book.book for user_book in user_books]
    })


@method_decorator(jwt_required, name='dispatch')
class AddBooksView(View):
    template_name = 'addbooks.html'

    def get(self, request):
        jwt_authenticator = JWTAuthentication()
        try:
            user, _ = jwt_authenticator.authenticate(request)
        except Exception:
            return redirect('/login/')

        if not user or user.is_anonymous:
            return redirect('/login/')

        form = BookForm()
        return render(request, self.template_name, {'form': form, 'title': 'Добавление книги'})

    def post(self, request):
        jwt_authenticator = JWTAuthentication()
        try:
            user, _ = jwt_authenticator.authenticate(request)
        except Exception:
            return redirect('/login/')

        if not user or user.is_anonymous:
            return redirect('/login/')

        # Обработка отправки формы
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = user  
            book.save()
            return redirect('/authenticated/')  

        return render(request, self.template_name, {'form': form, 'title': 'Добавление книги'})