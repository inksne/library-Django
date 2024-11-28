from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Book
from .serializers import BookSerializer, RegisterSerializer
from .decorators import jwt_required


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
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = (JWTAuthentication, )
    permission_classes = (IsAuthenticated, )


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


# @jwt_required
# def AuthenticatedView(request):
#     context = {
#         'title': 'Мои книги'
#     }
#     return render(request, 'mybooks.html', context)


@jwt_required
def UserBooksView(request):
    jwt_authenticator = JWTAuthentication()
    try:
        user, _ = jwt_authenticator.authenticate(request)
    except Exception:
        return redirect('/api/v1/login/')  

    if not user or user.is_anonymous:
        return redirect('/api/v1/login/') 

    books = Book.objects.filter(user=user)
    return render(request, 'mybooks.html', {'books': books, 'title': 'Мои книги'})